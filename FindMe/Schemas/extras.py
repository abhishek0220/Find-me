from FindMe.Schemas import user
from FindMe.Schemas import tasks


class GetSingleTask(tasks.SingleTask, tasks.TaskORMBase):
    author: user.UserInfo

    class Config:
        orm_mode = True
