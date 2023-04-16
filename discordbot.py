import discord
from discord.ext import commands
import os
import random
from datetime import datetime, timedelta
from xml.etree import ElementTree
import asyncio
import re
import requests
from bs4 import BeautifulSoup
import time
from difflib import SequenceMatcher
import json
import aiohttp
from saucenao_api import SauceNao
import io

folder_path = r"C:\동기화용\hit\hitomi_downloaded"
folder_name_pattern = r"\[(.*?)\] (.*?) \((.*?)\)"
recommend_folders = []



intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

"""token = 'MTA5NTAwNjc0NTA5ODcxOTI4Mw.Gp-Ze4.XOV5kaq0WPNNPzgPen1W_Glwzc2ewRUfOqC6Ec'"""

emoji_nong= '<:onimai6:1082291800577945660>'
emoji_nahida_nong = '<:nahida10:1046373960155136050>'
emoji_arisu = '<:arisu1:1084360920584699954>'
emoji_oo= '<:onimai11:1096330440043933757>'
emoji_xx= '<:onimai26:1096330475301257276>'
emoji_injung= '<:onimai13:1096330444506677259>'
emoji_pya= '<:onimai3:1082291767795273768>'
emoji_gd= '<:onimai15:1096330448692580392>'
emoji_qd= '<:onimai16:1096330450387087463>'
emoji_zalza= '<:onimai1:1082291760266494113>'
emoji_hhhh= '<:onimai5:1082291772669034629>'
emoji_ho='<:onimai12:1096330441625182269>'
emoji_stellazalza = '<:stella2:1048291981161402418>'
emoji_nanga= '<:onimai8:1082291774631989309>'
emoji_stella_hil= '<:stella3:1057574062295105587>'
@client.event
async def on_ready():
    game = discord.Game("한발 빼기")
    await client.change_presence(status=discord.Status.online, activity=game)
    channel = client.get_channel(1048578464875282493) # 채널 ID 입력
    async for message in channel.history(limit=5):
        for sticker in message.stickers:
            print(sticker.id,sticker.name)        
    print('Bot is ready.')
    
    """url = 'https://arca.live/b/bluearchive?category=%EC%A0%95%EB%B3%B4'
    latest_post_title = ''
    
    while True:
        # 0시 기준으로 다음 1시간을 계산합니다.
        now = datetime.now()
        next_send_time = datetime(now.year, now.month, now.day, now.hour, 0) + timedelta(hours=(now.minute // 1 + 1) * 1)
        # 다음 보내는 시간까지 대기합니다.
        wait_seconds = (next_send_time - now).total_seconds()
        channel = client.get_channel(1095613528708239440)
        await asyncio.sleep(wait_seconds)
        
        for i in range(6):
            directory = 'C:\동기화용\짤들'
            image_list = os.listdir(directory)
            delta = timedelta(hours=1)
            recent_files = []
            for file in image_list:
                file_path = os.path.join(directory, file)
                mtime = os.path.getmtime(file_path)
                file_time = datetime.fromtimestamp(mtime)
                if file_time > (now - delta):
                    recent_files.append(file)
            if not recent_files:
                await channel.send('오늘 저장된 짤이 없습니다.')
            else:
                selected_image = random.choice(recent_files)
                image_path = os.path.join(directory, selected_image)
                with open(image_path, 'rb') as f:
                    picture = discord.File(f, spoiler=True)
                    await channel.send('오늘 저장한짤 중 무작위로 보냅니다.')
                    sent_message = await channel.send(file=picture)
                    
        await asyncio.sleep(3600) # 1시간 (60초 x 60분)
            
        if now.hour == 23 and now.minute == 59:
            directory1 = 'C:\동기화용\짤들'
            directory2 = 'C:\동기화용\hit\hitomi_downloaded'
            delta = timedelta(hours=now.hour)
            recent_files1 = []
            recent_files2 = []
            for file in os.listdir(directory1):
                file_path = os.path.join(directory1, file)
                mtime = os.path.getmtime(file_path)
                file_time = datetime.fromtimestamp(mtime)
                if file_time > (now - delta):
                    recent_files1.append(file)
            for folder in os.listdir(directory2):
                folder_path = os.path.join(directory2, folder)
                mtime = os.path.getmtime(folder_path)
                folder_time = datetime.fromtimestamp(mtime)
                if folder_time > (now - delta):
                    recent_files2.append(folder)
            if not recent_files1 and not recent_files2:
                await channel.send('오늘 저장된 파일이 없습니다.')
            else:
                msg = f'현재 시간 기준 오늘 저장된 짤은 총 {len(recent_files1)}개의 짤과 {len(recent_files2)}개의 히토미입니다.'
                await message.channel.send(msg)
            await asyncio.sleep(60) # 60초(1분) 대기 후 다시 검사
        else:
            await asyncio.sleep(10) # 10초 대기 후 다시 검사"""
            


def get_random_image_url(character_name):
    search_url = f"https://safebooru.org/index.php?page=post&s=list&tags={character_name}"
    search_response = requests.get(search_url)
    soup = BeautifulSoup(search_response.content, 'html.parser')
    posts = soup.find_all('span', class_='thumb')
    if len(posts) == 0:
        return None
    random_post = posts[random.randint(0, len(posts)-1)]
    post_id = random_post.a['href'].split('=')[-1]
    thumbnail_url = random_post.img['src']
    post_url = f"https://safebooru.org/index.php?page=post&s=view&id={post_id}"
    return (thumbnail_url, post_url)



                
@client.event
async def on_message(message):
    """if message.content.startswith('!짤'):
        channel = message.channel
        directory = 'C:\동기화용\짤들'
        image_list = os.listdir(directory)
        selected_image = random.choice(image_list)
        image_path = os.path.join(directory, selected_image)
        with open(image_path, 'rb') as f:
            picture = discord.File(f, spoiler=True)
            sent_message = await channel.send('파일 안에 있는 짤 중 무작위로 보냅니다.', file=picture)
            await sent_message.add_reaction('🔁')
            await sent_message.add_reaction('👍')
            await sent_message.add_reaction('👎')
            await channel.send('🔁를 누르면 무작위로 다시 보냅니다')

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '🔁' and reaction.message.id == sent_message.id

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await sent_message.remove_reaction('🔁', client.user)
            else:
                await on_message(message)"""
    if message.content.startswith('!짤'):
        channel = message.channel
        directory = 'C:\동기화용\짤들'
        image_list = os.listdir(directory)
        selected_image = random.choice(image_list)
        image_path = os.path.join(directory, selected_image)
        with open(image_path, 'rb') as f:
            picture = discord.File(f, spoiler=True)
            sent_message = await channel.send('파일 안에 있는 짤 중 무작위로 보냅니다.', file=picture)
            await sent_message.add_reaction('🔁')
            await sent_message.add_reaction('🔍')
            await sent_message.add_reaction('👍')
            await sent_message.add_reaction('👎')
            await channel.send('작가 검색을 원하시면 🔍 누르거나 다시 짤을 받고 싶으면 🔁을 눌러주세요')


            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in ['🔁', '🔍'] and reaction.message.id == sent_message.id

            while True:
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await sent_message.remove_reaction('🔁', client.user)
                    break
                else:
                    if str(reaction.emoji) == '🔍':
                        try:
                            attachment_url = sent_message.attachments[0].url
                            
                            api_url = "https://saucenao.com/search.php"
                            params = {
                                "url": attachment_url,  # 검색할 이미지 링크
                                "output_type": 2,  # 검색 결과 타입 (2: 링크)
                                "api_key": "39f08dc2f8d7cc8dac80ad8ee9406306a053d176",  # Saucenao API 키
                            }
                            response = requests.get(api_url, params=params)
                            result = response.json()
                            pixiv_id = result["results"][0]["data"]["pixiv_id"]
                            member_name = result["results"][0]["data"]["member_name"]
                            member_id = result["results"][0]["data"]["member_id"]
                            print("pixiv id:", pixiv_id)
                            print("member name:", member_name)
                            print("member id:", member_id)
                            pixiv_link = "https://www.pixiv.net/artworks/{}".format(pixiv_id)
                            print("Pixiv artwork link:", pixiv_link)
                            await channel.send(pixiv_link)
                            break
                            
                        except asyncio.TimeoutError:
                            await channel.send('시간 내에 입력하지 않아 링크를 가져올 수 없습니다.')
                    else:
                        await on_message(message)

    """if message.content.startswith('!짤'):
        channel = message.channel
        directory = 'C:\동기화용\짤들'
        image_list = os.listdir(directory)
        selected_image = random.choice(image_list)
        image_path = os.path.join(directory, selected_image)
        with open(image_path, 'rb') as f:
            picture = discord.File(f, spoiler=True)
            sent_message = await channel.send('파일 안에 있는 짤 중 무작위로 보냅니다.', file=picture)
            await sent_message.add_reaction('🔁')
            await sent_message.add_reaction('👍')
            await sent_message.add_reaction('👎')
            await channel.send('🔁를 누르면 무작위로 다시 보냅니다')
            await channel.send(sent_message.attachments[0].url)
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '🔁' and reaction.message.id == sent_message.id

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await sent_message.remove_reaction('🔁', client.user)
            else:
                await channel.send(sent_message.attachments[0].url)
                        
    if message.content.startswith('!검색'):
        async for past_message in message.channel.history(limit=5):
            if past_message.attachments:
                attachment = past_message.attachments[0]
                if attachment.url.endswith(('png', 'jpeg', 'jpg', 'gif')):
                    await message.channel.send(attachment.url)
                    break
        else:
            await message.channel.send('최근에 전송된 이미지가 없습니다.')"""
        
   

                
    if message.content.startswith('!목록'):
        commands = ['!짤 = 저장된 짤 중에 랜덤으로 하나 보여줍니다. \n''!최근짤 = 3일 전부터 현재까지 저장된 짤 중에 랜덤으로 하나 보여줍니다. \n'
                    '!오늘의짤 = 1일 전부터 현재까지 저장된 짤 중에 랜덤으로 하나 보여줍니다. \n'
                    '!히토미추천 =  히토미 작품을 하나 추천합니다. \n''!오늘의히토미 = 1일 전부터 현재까지 저장된 작품 중에 랜덤으로 하나 보여줍니다. \n'
                    '!작가 작가이름 = 입력한 작가의 작품을 모두 불러옵니다. (DM으로 옴) \n'
                    '!작가검색 작가이름 = 이 작가가 폴더에 있는지 확인합니다. 만약 틀리거나 없으면 유사한 작가 이름을 보여줍니다. \n'
                    '!오늘의요약 = 오늘 저장된 짤 갯수와 히토미 작품의 갯수를 알려줍니다. \n'
                    '!다운로드된파일 = 현재 다운로드 된 짤 개수와 히토미 작품의 개수를 알려줍니다. \n''!목록 = 사용가능한 명령어를 알려줍니다. \n'] # 추가된 명령어 포함
        commands_str = ', '.join(commands)
        await message.channel.send('사용 가능한 명령어: \n' + commands_str)


    elif message.content.startswith('!청소'):
        if message.author.guild_permissions.administrator:
            try:
                amount = int(message.content.split(' ')[1])
                await message.channel.purge(limit=amount+1)
                
            except:
                await message.channel.send('메시지 삭제에 실패하였습니다.')
        else:
            await message.channel.send('관리자 권한이 필요합니다.')
            
    elif message.content.startswith('!최근짤'):
        current_activity = "최근짤 보내기"
        channel = message.channel
        directory = 'C:\동기화용\짤들'
        image_list = os.listdir(directory)
        now = datetime.now()
        delta = timedelta(days=3)
        recent_files = []
        for file in image_list:
            file_path = os.path.join(directory, file)
            mtime = os.path.getmtime(file_path)
            file_time = datetime.fromtimestamp(mtime)
            if file_time > (now - delta):
                recent_files.append(file)
        if not recent_files:
            await channel.send('최근 3일간 저장된 짤이 없습니다.')
        else:
            selected_image = random.choice(recent_files)
            image_path = os.path.join(directory, selected_image)
            with open(image_path, 'rb') as f:
                picture = discord.File(f, spoiler=True)
                await channel.send('3일전부터 지금까지 저장한짤 중 무작위로 보냅니다.')
                sent_message = await channel.send(file=picture)
                await sent_message.add_reaction('🔁')
                await sent_message.add_reaction('🔍')
                await sent_message.add_reaction('👍')
                await sent_message.add_reaction('👎')
                await channel.send('작가 검색을 원하시면 🔍 누르거나 다시 짤을 받고 싶으면 🔁을 눌러주세요')


                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) in ['🔁', '🔍'] and reaction.message.id == sent_message.id

                while True:
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        await sent_message.remove_reaction('🔁', client.user)
                        break
                    else:
                        if str(reaction.emoji) == '🔍':
                            try:
                                attachment_url = sent_message.attachments[0].url
                                
                                api_url = "https://saucenao.com/search.php"
                                params = {
                                    "url": attachment_url,  # 검색할 이미지 링크
                                    "output_type": 2,  # 검색 결과 타입 (2: 링크)
                                    "api_key": "39f08dc2f8d7cc8dac80ad8ee9406306a053d176",  # Saucenao API 키
                                }
                                response = requests.get(api_url, params=params)
                                result = response.json()
                                pixiv_id = result["results"][0]["data"]["pixiv_id"]
                                member_name = result["results"][0]["data"]["member_name"]
                                member_id = result["results"][0]["data"]["member_id"]
                                print("pixiv id:", pixiv_id)
                                print("member name:", member_name)
                                print("member id:", member_id)
                                pixiv_link = "https://www.pixiv.net/artworks/{}".format(pixiv_id)
                                print("Pixiv artwork link:", pixiv_link)
                                await channel.send(pixiv_link)
                                break
                                
                            except asyncio.TimeoutError:
                                await channel.send('시간 내에 입력하지 않아 링크를 가져올 수 없습니다.')
                        else:
                            await on_message(message)

                    
    if message.content.startswith('!오늘의짤'):
        channel = message.channel
        directory = 'C:\동기화용\짤들'
        image_list = os.listdir(directory)
        now = datetime.now()
        delta = timedelta(days=3)
        recent_files = []
        for file in image_list:
            file_path = os.path.join(directory, file)
            mtime = os.path.getmtime(file_path)
            file_time = datetime.fromtimestamp(mtime)
            if file_time > (now - delta):
                recent_files.append(file)
        if not recent_files:
            await channel.send('오늘 저장된 짤이 없습니다.')
        else:
            selected_image = random.choice(recent_files)
            image_path = os.path.join(directory, selected_image)
            with open(image_path, 'rb') as f:
                picture = discord.File(f, spoiler=True)
                sent_message = await channel.send('오늘 저장한 짤 중 무작위로 보냅니다.', file=picture)
                await sent_message.add_reaction('🔁')
                await sent_message.add_reaction('🔍')
                await sent_message.add_reaction('👍')
                await sent_message.add_reaction('👎')
                await channel.send('작가 검색을 원하시면 🔍 누르거나 다시 짤을 받고 싶으면 🔁을 눌러주세요')


                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) in ['🔁', '🔍'] and reaction.message.id == sent_message.id

                while True:
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        await sent_message.remove_reaction('🔁', client.user)
                        break
                    else:
                        if str(reaction.emoji) == '🔍':
                            try:
                                attachment_url = sent_message.attachments[0].url
                                
                                api_url = "https://saucenao.com/search.php"
                                params = {
                                    "url": attachment_url,  # 검색할 이미지 링크
                                    "output_type": 2,  # 검색 결과 타입 (2: 링크)
                                    "api_key": "39f08dc2f8d7cc8dac80ad8ee9406306a053d176",  # Saucenao API 키
                                }
                                response = requests.get(api_url, params=params)
                                result = response.json()
                                pixiv_id = result["results"][0]["data"]["pixiv_id"]
                                member_name = result["results"][0]["data"]["member_name"]
                                member_id = result["results"][0]["data"]["member_id"]
                                print("pixiv id:", pixiv_id)
                                print("member name:", member_name)
                                print("member id:", member_id)
                                pixiv_link = "https://www.pixiv.net/artworks/{}".format(pixiv_id)
                                print("Pixiv artwork link:", pixiv_link)
                                await channel.send(pixiv_link)
                                break
                                
                            except asyncio.TimeoutError:
                                await channel.send('시간 내에 입력하지 않아 링크를 가져올 수 없습니다.')
                        else:
                            await on_message(message)




                    
    if message.content.startswith('!청소'):
        if message.author.guild_permissions.administrator:
            try:
                amount = int(message.content.split(' ')[1])
                await message.channel.purge(limit=amount+1)
                
            except:
                await message.channel.send('메시지 삭제에 실패하였습니다.')
        else:
            await message.channel.send('관리자 권한이 필요합니다.')

    if message.content.startswith('!투표'):
        # !투표 다음에 입력된 내용을 가져옵니다.
        query = message.content[4:]

        # 이모지를 추가합니다.
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        await message.add_reaction('🤷')    


    if message.content.startswith('!히토미추천'):
        # 추천 폴더 경로 설정
        recommend_path = 'C:\\동기화용\\hit\\hitomi_downloaded'

        # 작가 이름에 따른 폴더 리스트 생성
        folders_by_artist = {}
        for folder_name in os.listdir(recommend_path):
            match = re.search(r'\[(.+?)\]', folder_name)
            if match:
                artist_name = match.group(1)
                if artist_name not in folders_by_artist:
                    folders_by_artist[artist_name] = []
                folders_by_artist[artist_name].append(folder_name)

        # 작가 이름 랜덤 선택 및 해당 작가의 폴더 리스트에서 폴더 랜덤 선택
        artist_name = random.choice(list(folders_by_artist.keys()))
        folder_name = random.choice(folders_by_artist[artist_name])

        # 폴더 이름에서 작가 이름, 제목, 번호 추출
        folder_name_pattern = r'\[(.+?)\]\s(.+?)\s\((\d+)\)'
        match = re.search(folder_name_pattern, folder_name)
        artist_name = match.group(1)
        title = match.group(2)
        number = int(match.group(3))

        # 추천 정보 출력
        recommend_info = f'작가: {artist_name}\n제목: {title}\n번호: {number}'
        await message.channel.send(recommend_info)

        # 폴더 내 첫 번째 이미지 파일 경로 설정
        folder_path = os.path.join(recommend_path, folder_name)
        image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".webp")]
        first_image_path = os.path.join(folder_path, image_files[0])

        # 이미지 파일 전송
        with open(first_image_path, 'rb') as f:
            picture = discord.File(f, spoiler=True)
            await message.channel.send(file=picture)

    if message.content.startswith('!작가'):
        # 작가 이름 추출
        author_name = message.content[4:].strip()

        # 추천 폴더 경로 설정
        recommend_path = 'C:\\동기화용\\hit\\hitomi_downloaded'

        # 작가 이름에 해당하는 폴더 리스트 생성
        folders_by_author = [f for f in os.listdir(recommend_path) if f.startswith(f'[{author_name}]')]

        # 해당 작가의 모든 폴더에서 정보 추출
        for folder_name in folders_by_author:
            # 폴더 이름에서 작가 이름, 제목, 번호 추출
            folder_name_pattern = r'\[(.+?)\]\s(.+?)\s\((\d+)\)'
            match = re.search(folder_name_pattern, folder_name)
            artist_name = match.group(1)
            title = match.group(2)
            number = int(match.group(3))

            # 추천 정보 출력
            recommend_info = f'작가: {artist_name}\n제목: {title}\n번호: {number}'
            await message.author.send(recommend_info)

            # 폴더 내 첫 번째 이미지 파일 경로 설정
            folder_path = os.path.join(recommend_path, folder_name)
            image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".webp")]
            first_image_path = os.path.join(folder_path, image_files[0])

            # 이미지 파일 전송
            with open(first_image_path, 'rb') as f:
                picture = discord.File(f, spoiler=True)
                await message.author.send(file=picture)

    """if message.content.startswith('!작가검색'):
        # 작가 이름 추출
        author_name = message.content[6:].strip()

        # 추천 폴더 경로 설정
        recommend_path = 'C:\\동기화용\\hit\\hitomi_downloaded'

        # 작가 이름에 해당하는 폴더 리스트 생성
        folders_by_author = [f for f in os.listdir(recommend_path) if f.lower().startswith(f'[{author_name.lower()}]')]

        if folders_by_author:
            # 해당 작가의 모든 폴더에서 정보 추출
            for folder_name in folders_by_author:
                # 폴더 이름에서 작가 이름 추출
                folder_name_pattern = r'\[(.+?)\]'
                match = re.search(folder_name_pattern, folder_name)
                artist_name = match.group(1)

                # 작가 이름 대소문자 구분 없이 비교
                if artist_name.lower() == author_name.lower():
                    await message.channel.send(f'작가: {artist_name}')
                    break

            await message.channel.send('작가가 존재합니다.')
        else:
            await message.channel.send('작가가 존재하지 않습니다.')"""

    if message.content.startswith('!작가검색'):
        # 작가 이름 추출
        author_name = message.content[6:].strip()

        # 추천 폴더 경로 설정
        recommend_path = 'C:\\동기화용\\hit\\hitomi_downloaded'

        # 작가 이름에 해당하는 폴더 리스트 생성
        folders_by_author = [f for f in os.listdir(recommend_path) if f.lower().startswith(f'[{author_name.lower()}]')]

        # 입력한 작가 이름과 유사한 작가 이름이 있는지 확인
        similar_author_names = []
        for folder_name in os.listdir(recommend_path):
            folder_name_pattern = r'\[(.+?)\]'
            match = re.search(folder_name_pattern, folder_name)
            if match:
                artist_name = match.group(1)
                similarity = SequenceMatcher(None, author_name.lower(), artist_name.lower()).ratio()
                if similarity >= 0.6 and artist_name not in similar_author_names:
                    similar_author_names.append(artist_name)

        if folders_by_author:
            # 해당 작가의 모든 폴더에서 정보 추출
            for folder_name in folders_by_author:
                # 폴더 이름에서 작가 이름 추출
                folder_name_pattern = r'\[(.+?)\]'
                match = re.search(folder_name_pattern, folder_name)
                artist_name = match.group(1)

                # 작가 이름 대소문자 구분 없이 비교
                if artist_name.lower() == author_name.lower():
                    await message.channel.send(f'작가: {artist_name}')
                    break

            await message.channel.send('작가가 존재합니다.')
        elif similar_author_names:
            await message.channel.send(f'입력한 작가 이름과 유사한 작가 이름: {", ".join(similar_author_names[:1])}')
        else:
            await message.channel.send('작가가 존재하지 않습니다.')
            
    if message.content.startswith('!오늘의요약'):
        directory1 = 'C:\동기화용\짤들'
        directory2 = 'C:\동기화용\hit\hitomi_downloaded'
        now = datetime.now()
        delta = timedelta(hours=now.hour)
        recent_files1 = []
        recent_files2 = []
        for file in os.listdir(directory1):
            file_path = os.path.join(directory1, file)
            mtime = os.path.getmtime(file_path)
            file_time = datetime.fromtimestamp(mtime)
            if file_time > (now - delta):
                recent_files1.append(file)
        for folder in os.listdir(directory2):
            folder_path = os.path.join(directory2, folder)
            mtime = os.path.getmtime(folder_path)
            folder_time = datetime.fromtimestamp(mtime)
            if folder_time > (now - delta):
                recent_files2.append(folder)
        if not recent_files1 and not recent_files2:
            await message.channel.send('오늘 저장된 파일이 없습니다.')
        else:
            msg = f'오늘 날짜 기준 0시부터 현재 시간까지 저장된 짤은 총 {len(recent_files1)}개 이고, 저장된 히토미 작품의 개수는 {len(recent_files2)}개 입니다.'
            await message.channel.send(msg)
    if message.content.startswith('!다운로드된파일'):
        directory1 = 'C:\동기화용\짤들'
        directory2 = 'C:\동기화용\hit\hitomi_downloaded'
        image_list = os.listdir(directory1)
        folder_list = os.listdir(directory2)
        image_count = len(image_list)
        folder_count = len(folder_list)
        msg1 = f'총 {image_count}개의 짤 이, 총 {folder_count}개의 히토미 작품이 있습니다.'
        await message.channel.send(msg1)

    if message.content.startswith('!오늘의히토미'):
        # 추천 폴더 경로 설정
        recommend_path = 'C:\\동기화용\\hit\\hitomi_downloaded'

        # 오늘 저장된 폴더 리스트 생성
        now = datetime.now()
        delta = timedelta(hours=now.hour)
        folders_today = []
        for folder_name in os.listdir(recommend_path):
            folder_path = os.path.join(recommend_path, folder_name)
            mtime = os.path.getmtime(folder_path)
            folder_time = datetime.fromtimestamp(mtime)
            if folder_time > (now - delta):
                folders_today.append(folder_name)
    
        if not folders_today:
            await message.channel.send('오늘 저장된 히토미가 없습니다.')
        else:
            # 폴더 랜덤 선택
            folder_name = random.choice(folders_today)

            # 폴더 이름에서 작가 이름, 제목, 번호 추출
            folder_name_pattern = r'\[(.+?)\]\s(.+?)\s\((\d+)\)'
            match = re.search(folder_name_pattern, folder_name)
            artist_name = match.group(1)
            title = match.group(2)
            number = int(match.group(3))

            # 추천 정보 출력
            recommend_info = f'작가: {artist_name}\n제목: {title}\n번호: {number}'
            await message.channel.send(recommend_info)

            # 폴더 내 첫 번째 이미지 파일 경로 설정
            folder_path = os.path.join(recommend_path, folder_name)
            image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".webp")]
            first_image_path = os.path.join(folder_path, image_files[0])

            # 이미지 파일 전송
            with open(first_image_path, 'rb') as f:
                picture = discord.File(f, spoiler=True)
                await message.channel.send(file=picture)

    if message.content.startswith('!캐릭터검색'):
        search_terms = message.content.split()[1:]
        if 'kokona' in search_terms:
            search_terms[search_terms.index('kokona')] = 'kokona_(blue_archive)'
        search_url = "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=200&tags=" + '_'.join(search_terms)

        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'xml')

        # find the posts
        posts = soup.find_all('post')
        if not posts:
            await message.channel.send('검색 결과가 없습니다.')
            return

        # select a random post
        post = random.choice(posts)

        # get the post thumbnail and link
        thumbnail_url = post.get('preview_url')
        post_url = 'https://safebooru.org/index.php?page=post&s=view&id=' + post.get('id')

        # send the thumbnail and link
        embed = discord.Embed(title='검색 결과', url=post_url)
        embed.set_image(url=thumbnail_url)
        await message.channel.send(embed=embed)

            
    if '농ㅋㅋ' in message.content or '농 ㅋㅋ' in message.content or 'shdzz' in message.content or 'nongzz' in message.content or 'Shdzz' in message.content:
        await message.reply(random.choice([emoji_nong, emoji_nahida_nong, emoji_arisu]))   
    if message.content.endswith('ㅇㅈ?'):
        await message.reply(emoji_injung)
    if message.content.endswith('싶다'):
        await message.reply(random.choice([emoji_oo, emoji_injung, emoji_pya, emoji_hhhh]))
    if message.content.endswith('함?'):
        await message.reply(random.choice([emoji_oo, emoji_xx]))
    if message.content.endswith('아님'):
        await message.reply(random.choice([emoji_oo, emoji_xx]))
    if message.content.endswith('임?'):
        await message.reply(random.choice([emoji_oo, emoji_xx]))
    if message.content.endswith('없지'):
        await message.reply(random.choice([emoji_oo, emoji_injung, emoji_xx]))
    if message.content.endswith('노?') or message.content.endswith('노ㅋㅋ') or message.content.endswith('노') or message.content.endswith('노 ㅋㅋ'):
        await message.reply(random.choice([emoji_hhhh, emoji_ho]))        
    if message.content.endswith('마렵네') or message.content.endswith('마렵다'):
        await message.reply(random.choice([emoji_oo, emoji_injung,emoji_pya,emoji_hhhh,emoji_xx]))
    if message.content.endswith('ㄱ?'):
        await message.reply(random.choice([emoji_oo, emoji_injung]))
    if message.content.endswith('수구'):
        await message.reply(random.choice([emoji_oo, emoji_xx]))
    if message.content.endswith('해주셈') or message.content.endswith('해주샘') or message.content.endswith('해줘'):
        await message.reply(random.choice([emoji_oo, emoji_xx]))
    if message.content.endswith('디질래요') or message.content.endswith('디질래요?'):
        await message.reply(random.choice([emoji_oo, emoji_xx, emoji_hhhh]))        
    if message.content.endswith('님') or message.content.endswith('님아'): 
        await message.reply(random.choice([emoji_oo, emoji_nanga]))
    if message.content.endswith('죽임'):
        await message.reply(random.choice([emoji_oo, emoji_xx,emoji_hhhh]))
        
    if message.author == client.user: 
        return
    
    for sticker in message.stickers: 
        if sticker.id == 1094463583821254696 and sticker.name == "호시노잘자": 
            await message.reply(random.choice([emoji_zalza,emoji_stellazalza]))
            break

    for sticker in message.stickers: 
        if sticker.id == 1087366995323932694 and sticker.name == "농 ㅋㅋ": 
            await message.reply(random.choice([emoji_injung,emoji_xx]))
            break
    for sticker in message.stickers: 
        if sticker.id == 1087379566806454373 and sticker.name == "농 ㅋㅋㅋ": 
            await message.reply(random.choice([emoji_injung,emoji_xx]))
            break    
client.run(os.environ['token'])
