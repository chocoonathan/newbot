import random
import string
from typing import List, Set

n = "\n"
w = " "

bold = lambda x: f"**{x}:** "
bold_ul = lambda x: f"**--{x}:**-- "

mono = lambda x: f"`{x}`{n}"


def section(
    title: str,
    body: dict,
    indent: int = 2,
    underline: bool = False,
) -> str:
    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        if value is not None:
            text += (
                indent * w
                + bold(key)
                + (
                    (value[0] + n)
                    if isinstance(value, list) and isinstance(value[0], str)
                    else mono(value)
                )
            )
    return text


class TaskManager:
    active_tasks: Set[str] = set()

    @staticmethod
    def generate_task_id(length: int = 8) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    @classmethod
    def start_task(cls) -> str:
        task_id = cls.generate_task_id()
        cls.active_tasks.add(task_id)
        return task_id

    @classmethod
    def end_task(cls, task_id: str) -> None:
        cls.active_tasks.discard(task_id)

    @classmethod
    def is_active(cls, task_id: str) -> bool:
        return task_id in cls.active_tasks

    @classmethod
    def get_active_tasks(cls) -> List[str]:
        """
        Mengembalikan daftar task ID yang aktif.
        """
        return list(cls.active_tasks)


task = TaskManager()
