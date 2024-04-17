import os
import pandas as pd

from tempfile import NamedTemporaryFile


class ExcelExportService:
    """Сервис для экспорта данных в Excel."""
    base_file_name: str = "statistics"

    def export_to_excel(self, data, sheet_name='Sheet1'):
        """Экспорт данных во временный Excel файл."""
        df = pd.DataFrame(data)
        with NamedTemporaryFile(delete=False, suffix='.xlsx', dir=os.path.join('tmp'), prefix='stat_') as tmp:
            with pd.ExcelWriter(tmp.name, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            return tmp.name