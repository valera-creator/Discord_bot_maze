import discord
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "TOKEN"


class YLBotClient(discord.Client):

    def __init__(self, intents):
        super().__init__(intents=intents)
        self.game_status = ''

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.game_status == '' or self.game_status == 'end':
            self.game_status = '1'
            await message.channel.send("Вы находитесь в лабиринте. Чтобы выбраться из него, "
                                       "вам нужно войти в дверь. Но где она - "
                                       "неизвестно.\nВы находитесь в комнате 1. Из нее есть двери в комнаты 5, 2, 3. "
                                       "Какую веберете?")
            return

        if self.game_status == '1':
            if message.content == '3':
                await message.channel.send("У вас есть выбор: пойти в 4 дверь или вернуться в 1. Что выберете?")
                self.game_status = '3'
                return

            elif message.content == '2':
                await message.channel.send("Вы в тупике. Чтобы вернуться в комнату 1, введите 1.")
                self.game_status = '2'
                return

            elif message.content == '5':
                await message.channel.send("Вы не можете вернуться к двери 1, т.к. пропуск был одноразовый. "
                                           "Теперь вы можете только пойти в 9")
                self.game_status = '5'
                return
            else:
                await message.channel.send('Неверный ход! Есть только двери в комнаты 5, 2, 3. Какую веберете?')
                return

        elif self.game_status == '5':
            if message.content != '9':
                await message.channel.send('Неверный ход! Теперь вы можете только пойти в 9')
                return
            else:
                self.game_status = '9'
                await message.channel.send("Перед вами выбор: 5 комната или 8 комната или комната 7. Что выберете?")
                return

        elif self.game_status == '2':
            if message.content != '1':
                await message.channel.send("Неверный ход! Вы в тупике. Чтобы вернуться в комнату 1, введите 1.")
                return
            else:
                self.game_status = '1'
                await message.channel.send('Перед вами комнады 5, 2, 3. Какую веберете?')
                return

        elif self.game_status == '3':
            if message.content != '1' and message.content != '4':
                await message.channel.send('Неверный ход! У вас есть выбор: пойти в 4 дверь или вернуться в 1. '
                                           'Что выберете?')
                return

            if message.content == '1':
                self.game_status = '1'
                await message.channel.send('Перед вами комнады 5, 2, 3. Какую веберете?')
                return

            elif message.content == '4':
                self.game_status = '4'
                await message.channel.send("У вас есть выбор: 6 или 3. Что выберете?")
                return

        elif self.game_status == '4':
            if message.content != '6' and message.content != '3':
                await message.channel.send('Неверный ход! У вас есть выбор: пойти в 6 дверь или вернуться в 3. '
                                           'Что выберете?')
                return

            if message.content == '6':
                await message.channel.send('Ура! Вы выбрались! Пока! Если хотите еще раз сыграть, напишите)')
                self.game_status = 'end'
                return

            elif message.content == '3':
                await message.channel.send("У вас есть выбор: пойти в 4 дверь или вернуться в 1. Что выберете?")
                self.game_status = '3'
                return

        elif self.game_status == '9':

            if message.content != '5' and message.content != '8' and message.content != '7':
                await message.channel.send('Неверный ход! Вы можете выбрать только 5, 8, 7 комнаты')
                return

            if message.content == '5':
                await message.channel.send('Вы перешли в комнату 5. Но у вас нет других выходов, кроме в комнату 9\n'
                                           'Выберите 9')
                self.game_status = '5'
                return

            if message.content == '7':
                self.game_status = '7'
                await message.channel.send("Мост обрушился и остался путь, который ведет в комнату 8. Введите 8.")
                return

            if message.content == '8':
                await message.channel.send('Вы умерли! Если хотите еще раз сыграть, напишите)')
                self.game_status = 'end'
                return

        elif self.game_status == '7':
            if message.content != '8':
                await message.channel.send('Неверный ход! Вы обрушили мост и теперь можете пойти только в комнату 8.')
                return
            if message.content == '8':
                await message.channel.send('Вы умерли! Если хотите еще раз сыграть, напишите)')
                self.game_status = 'end'
                return


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents)
client.run(TOKEN)
