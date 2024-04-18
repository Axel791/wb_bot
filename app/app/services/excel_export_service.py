import os
import pandas as pd

from tempfile import NamedTemporaryFile


class ExcelExportService:
    """Сервис для экспорта данных в Excel."""

    def export_to_excel(self, data, sheet_name='Sheet1'):
        """Экспорт данных во временный Excel файл."""
        df = pd.DataFrame(data)

        temp_dir = os.path.join('/app', 'tmp')
        os.makedirs(temp_dir, exist_ok=True)

        # Создание временного файла
        with NamedTemporaryFile(delete=False, suffix='.xlsx', dir=temp_dir, prefix='stat_') as tmp:
            with pd.ExcelWriter(tmp.name, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            return tmp.file