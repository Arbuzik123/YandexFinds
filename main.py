import asyncio
from Searchengines.startFind import YandexFind
async def main():
    price = 'result.xlsx'
    await YandexFind(price)
    # await createFilesYandex(price)#Вставка пути к файлу Yandex
if __name__ == '__main__':
    asyncio.run(main())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
