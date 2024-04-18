import os
import aioredis

from aiogram import F
from aiogram.types import FSInputFile
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.states.state import StatForm
from app.keyboards.keyboard import yes_no_kb, cancel_kb

from app.services.supplier_stat_service import SupplierStatService, StatType
from app.services.excel_export_service import ExcelExportService
from app.services.statics_api_service import StatisticsAPIService

stat_router = Router()


@stat_router.callback_query(F.data == "get_stat")
@inject
async def send_date(
        callback_query: CallbackQuery,
        state: FSMContext,
        redis: aioredis.Redis = Provide[Container.redis_pool]
) -> None:
    """Принимаем последнего изменения по поставке"""
    user_id = str(callback_query.from_user.id)

    if await redis.exists(user_id):
        await callback_query.message.answer("Ограничение 3 минуты на просмотр статистики")
        return

    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(
        "Введите дату и время последнего изменения по поставке\n Формат: 2019-06-20 или 2017-03-25T00:00:00",
        reply_markup=cancel_kb,
    )

    await state.set_state(StatForm.date_from)


@stat_router.message(StatForm.date_from)
async def process_date(message: Message, state: FSMContext) -> None:
    """Обработка введенной даты"""
    msg = message.text
    await state.update_data(date=msg)

    await message.answer("Используем флаг?", reply_markup=yes_no_kb)
    await state.set_state(StatForm.flag)


@stat_router.callback_query(StatForm.flag)
@inject
async def process_stat(
        callback_query: CallbackQuery,
        state: FSMContext,
        supplier_stat_service: SupplierStatService = Provide[Container.supplier_stat_service],
        excel_export_service: ExcelExportService = Provide[Container.excel_export_service],
        statics_api_service: StatisticsAPIService = Provide[Container.statics_api_service],
        redis: aioredis.Redis = Provide[Container.redis_pool]
) -> None:
    """Отдаем статистику пользователю"""
    callback_query_msg = callback_query.message
    user_id = str(callback_query.from_user.id)

    if callback_query_msg == "cancel":
        await state.clear()
        return

    flag = 1 if callback_query_msg == "yes" else 0
    data = await state.get_data()

    date_from = data.get("date")

    stats_sale = await statics_api_service.get_sales_data(date_from=date_from, flag=flag)
    stats_order = await statics_api_service.get_orders_data(date_from=date_from, flag=flag)

    if stats_sale:
        validated_stat_sale = await supplier_stat_service.validate_exist_stat_item(
            objs=stats_sale,
            stat_type=StatType.sales
        )
        if validated_stat_sale:
            await supplier_stat_service.create_supplier_sale_stat(objs=validated_stat_sale)
            sales_exel_file = excel_export_service.export_to_excel(data=validated_stat_sale)

            file = FSInputFile(sales_exel_file)
            await callback_query.message.answer_document(file, caption='Продажи')

            os.remove(sales_exel_file)

    if stats_order:
        validated_stat_order = await supplier_stat_service.validate_exist_stat_item(
            objs=stats_order,
            stat_type=StatType.orders
        )
        if validated_stat_order:
            await supplier_stat_service.create_supplier_orders_stat(objs=validated_stat_order)
            orders_excel_file = excel_export_service.export_to_excel(data=validated_stat_order)
            file = FSInputFile(orders_excel_file)
            await callback_query.message.answer_document(file, caption='Заказы')

            os.remove(orders_excel_file)

    await redis.set(user_id, "active", ex=180)
    await state.clear()
    await statics_api_service.close()


@stat_router.callback_query(F.data == "cancel")
async def cancel(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Отмена действия"""
    await callback_query.message.delete_reply_markup()
    await state.clear()
    await callback_query.message.answer(
        "Действие отменено.",
    )
