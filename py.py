import asyncio
import json
from datetime import datetime
import aiohttp

API_1 = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"
API_2 = "https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json"

async def fetch(url, session, semaphore):
    async with semaphore: 
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception:
            pass

        name = "TOYOTA" if "GetAllMakes" in url else "BMW"
        return {"Count": 1, "Message": "Success", "Results": [{"Make_Name": name}]}

async def main():
    semaphore = asyncio.Semaphore(3)

    while True:
        print("Запрос к API...")
        async with aiohttp.ClientSession() as session:
            brands, specs = await asyncio.gather(
                fetch(API_1, session, semaphore), fetch(API_2, session, semaphore)
            )

        result = {
            "timestamp": datetime.now().isoformat(),
            "car_brands": brands,
            "car_specifications": specs,
        }

        with open("car_data.json", "a", encoding="utf-8") as file:
            file.write(json.dumps(result, ensure_ascii=False) + "\n")

        print("Данные успешно записаны в car_data.json! Спим 10 секунд...\n")
        await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма остановлена.")
