from aiogram.dispatcher.handler import SkipHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import Dispatcher, types
from datetime import datetime as dt
from bot.config import STATE_EXPIRE_TIME_IN_SEC as EXPIRE_TIME_SECONDS


class StateValidationMiddleware(BaseMiddleware):
    def __init__(self):
        super(StateValidationMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
            Check if state is expired, if so middleware removes
            the state and skips the current handler.
        """
        dp = Dispatcher.get_current()
        state = dp.current_state()
        data = await state.get_data()

        if 'time' in data:
            # print('time is here!')
            time_delta = (dt.now() - data['time']).total_seconds()
            if time_delta >= EXPIRE_TIME_SECONDS:
                await state.reset_state()
                # TODO: create massage for that.
                await message.answer("Вы отвечали слишко долго. Предыдущая операция отмена. Вызываю команду /start.")
                # print('State were removed.')
                raise SkipHandler()

        n = dt.now()
        await state.update_data(time=n)
        # print("For user {} time set to {}.".format(message.from_user.username, n))
        # print(await state.get_state())
