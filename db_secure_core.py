import sqlite3
import threading
import logging
from typing import Any, List, Tuple, Optional, Union

# 🔧 إعداد نظام التسجيل (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 🔒 قاموس للأقفال المنفصلة لكل قاعدة بيانات (أفضل من قفل واحد لكل شيء)
_locks: dict[str, threading.Lock] = {}
_locks_lock = threading.Lock()


def _get_db_lock(db_path: str) -> threading.Lock:
    """الحصول على قفل مخصص لقاعدة البيانات المحددة."""
    with _locks_lock:
        if db_path not in _locks:
            _locks[db_path] = threading.Lock()
        return _locks[db_path]


def execute_secure_query(
    db_path: str,
    query: str,
    params: Union[Tuple, List, dict] = (),
    is_select: bool = False,
    is_executemany: bool = False,
    has_returning: bool = False
) -> Optional[Union[List[Tuple], int, bool]]:
    """
    محرك تنفيذ العمليات البرمجية بشكل تتابعي آمن لمنع خطأ Database is Locked.

    Args:
        db_path: مسار ملف قاعدة البيانات.
        query: جملة SQL المراد تنفيذها.
        params: المعاملات (لمنع حقن SQL).
        is_select: True إذا كان الاستعلام SELECT.
        is_executemany: True إذا كنت تستخدم executemany (للإدراج المتعدد).
        has_returning: True إذا كانت الجملة تحتوي على RETURNING.

    Returns:
        - نتائج SELECT كقائمة من الصفوف.
        - عدد الصفوف المتأثرة للعمليات الأخرى.
        - None في حالة حدوث خطأ.
    """
    lock = _get_db_lock(db_path)

    with lock:
        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect(db_path, timeout=20.0)
            cursor = conn.cursor()

            if is_executemany:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)

            if is_select or has_returning:
                result = cursor.fetchall()
                conn.commit()
                return result
            else:
                conn.commit()
                return cursor.rowcount

        except sqlite3.OperationalError as e:
            logger.error(f"❌ خطأ تشغيلي في قاعدة البيانات: {e}")
            return None
        except sqlite3.IntegrityError as e:
            logger.error(f"❌ خطأ في سلامة البيانات: {e}")
            return None
        except sqlite3.Error as e:
            logger.error(f"❌ خطأ في قاعدة البيانات: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ خطأ غير متوقع: {e}")
            return None
        finally:
            if conn:
                conn.close()


def init_database(db_path: str, schema: str) -> bool:
    """
    تهيئة قاعدة البيانات بتنفيذ جمل DDL.

    Args:
        db_path: مسار ملف قاعدة البيانات.
        schema: جمل SQL لإنشاء الجداول.

    Returns:
        True إذا نجحت العملية، False إذا فشلت.
    """
    lock = _get_db_lock(db_path)

    with lock:
        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect(db_path, timeout=20.0)
            cursor = conn.cursor()
            cursor.executescript(schema)
            conn.commit()
            logger.info(f"✅ تم تهيئة قاعدة البيانات: {db_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"❌ فشل في تهيئة قاعدة البيانات: {e}")
            return False
        finally:
            if conn:
                conn.close()


def test_database_connection(db_path: str) -> bool:
    """
    اختبار الاتصال بقاعدة البيانات والتأكد من أنها تعمل.

    Args:
        db_path: مسار ملف قاعدة البيانات.

    Returns:
        True إذا كان الاتصال ناجحاً، False إذا فشل.
    """
    try:
        conn = sqlite3.connect(db_path, timeout=5.0)
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        conn.close()
        logger.info(f"✅ الاتصال بقاعدة البيانات ناجح (SQLite v{version})")
        return True
    except sqlite3.Error as e:
        logger.error(f"❌ فشل الاتصال بقاعدة البيانات: {e}")
        return False