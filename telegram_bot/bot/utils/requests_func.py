import asyncio
from bot.core.config import GET_PLACE_URL, GET_COORDINATES_URL, GRAPHQL_URL
from bot.queries.cameras import query_parse, full_general_report
import aiohttp

async def get_info(camera_id: int):
    async with aiohttp.ClientSession() as session:
        async def camera_info():
            async with session.post(GRAPHQL_URL, json={"query": query_parse(camera_id)}) as response:
                response_camera = await response.json()
                return response_camera
        async def coordinates_info():
            async with session.get(f"{GET_COORDINATES_URL}/{camera_id}") as response:
                response_coordinates = await response.json()
                return response_coordinates
        async def place_info():
            async with session.get(f"{GET_PLACE_URL}/{camera_id}") as response:
                response_place = await response.json()
                return response_place
            
        response_camera, response_coordinates, response_place = await asyncio.gather(
            camera_info(),
            coordinates_info(),
            place_info()
        )
        return response_camera, response_coordinates, response_place


async def get_full_cor_res_info():
    async with aiohttp.ClientSession() as session:

        async def camera_1():
            async def get_cor():
                async with session.get(f"{GET_COORDINATES_URL}/1") as response:
                    return await response.json()
            async def get_place():
                async with session.get(f"{GET_PLACE_URL}/1") as response:
                    return await response.json()
            return await asyncio.gather(get_cor(), get_place())
        
        async def camera_2():
            async def get_cor():
                async with session.get(f"{GET_COORDINATES_URL}/2") as response:
                    return await response.json()
            async def get_place():
                async with session.get(f"{GET_PLACE_URL}/2") as response:
                    return await response.json()
            return await asyncio.gather(get_cor(), get_place())
        

        async def camera_3():
            async def get_cor():
                async with session.get(f"{GET_COORDINATES_URL}/3") as response:
                    return await response.json()
            async def get_place():
                async with session.get(f"{GET_PLACE_URL}/3") as response:
                    return await response.json()
            return await asyncio.gather(get_cor(), get_place())
        

        async def camera_4():
            async def get_cor():
                async with session.get(f"{GET_COORDINATES_URL}/4") as response:
                    return await response.json()
            async def get_place():
                async with session.get(f"{GET_PLACE_URL}/4") as response:
                    return await response.json()
            return await asyncio.gather(get_cor(), get_place())
        
        async def camera_5():
            async def get_cor():
                async with session.get(f"{GET_COORDINATES_URL}/5") as response:
                    return await response.json()
            async def get_place():
                async with session.get(f"{GET_PLACE_URL}/5") as response:
                    return await response.json()
            return await asyncio.gather(get_cor(), get_place())

        camera_1_info, camera_2_info, camera_3_info, camera_4_info,camera_5_info = await asyncio.gather(
            camera_1(),
            camera_2(),
            camera_3(),
            camera_4(),
            camera_5()
        )

        return camera_1_info, camera_2_info, camera_3_info, camera_4_info, camera_5_info
    
async def get_full_and_info_final():
    async def graph_full():
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAPHQL_URL, json={"query": full_general_report}) as response:
                response = await response.json()
                return response
    full_response, full_cor_res = await asyncio.gather(
        graph_full(),
        get_full_cor_res_info()
    )
    return full_response, full_cor_res