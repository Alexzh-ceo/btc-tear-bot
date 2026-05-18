{\rtf1\ansi\ansicpg1251\cocoartf2869
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import asyncio\
import os\
from datetime import datetime\
from aiogram import Bot\
from apscheduler.schedulers.asyncio import AsyncIOScheduler\
from openai import AsyncOpenAI\
\
# ================= \uc0\u1053 \u1040 \u1057 \u1058 \u1056 \u1054 \u1049 \u1050 \u1048  =================\
BOT_TOKEN = "\uc0\u1058 \u1054 \u1050 \u1045 \u1053 _\u1054 \u1058 _BOTFATHER"\
GROK_API_KEY = "xai-\uc0\u1090 \u1074 \u1086 \u1081 _\u1082 \u1083 \u1102 \u1095 _\u1079 \u1076 \u1077 \u1089 \u1100 "\
CHANNEL_ID = "@btctear"   # \uc0\u1080 \u1083 \u1080  -1001234567890 (\u1095 \u1080 \u1089 \u1083 \u1086 \u1074 \u1086 \u1081  ID \u1082 \u1072 \u1085 \u1072 \u1083 \u1072 )\
\
# \uc0\u1057 \u1080 \u1089 \u1090 \u1077 \u1084 \u1085 \u1099 \u1081  \u1087 \u1088 \u1086 \u1084 \u1087 \u1090  (\u1090 \u1074 \u1086 \u1081  \u1089 \u1090 \u1080 \u1083 \u1100 )\
SYSTEM_PROMPT = """\
\uc0\u1058 \u1099  \'97 \u1075 \u1083 \u1072 \u1074 \u1085 \u1099 \u1081  \u1088 \u1077 \u1076 \u1072 \u1082 \u1090 \u1086 \u1088  \u1093 \u1072 \u1081 \u1087 \u1086 \u1074 \u1086 \u1075 \u1086  \u1082 \u1088 \u1080 \u1087 \u1090 \u1086 -\u1082 \u1072 \u1085 \u1072 \u1083 \u1072  BTC tear.  \
\uc0\u1057 \u1090 \u1080 \u1083 \u1100 : 60% \u1084 \u1086 \u1097 \u1085 \u1099 \u1081  \u1093 \u1072 \u1081 \u1087  + \u1101 \u1084 \u1086 \u1076 \u1079 \u1080  \u55357 \u56960 \u55357 \u56520 \u55357 \u56485 , 30% \u1089 \u1077 \u1088 \u1100 \u1105 \u1079 \u1085 \u1099 \u1077  \u1073 \u1086 \u1083 \u1100 \u1096 \u1080 \u1077  \u1085 \u1086 \u1074 \u1086 \u1089 \u1090 \u1080 , 10% \u1089 \u1087 \u1077 \u1082 \u1091 \u1083 \u1103 \u1090 \u1080 \u1074 \u1085 \u1099 \u1077  \u1080 \u1085 \u1089 \u1072 \u1081 \u1076 \u1099  (\'ab\u1080 \u1085 \u1089 \u1072 \u1081 \u1076 \u1077 \u1088 \u1099  \u1096 \u1077 \u1087 \u1095 \u1091 \u1090 \'bb, \'ab\u1072  \u1095 \u1090 \u1086  \u1077 \u1089 \u1083 \u1080 \'85\'bb, \'ab\u1084 \u1086 \u1078 \u1077 \u1090  \u1074 \u1079 \u1083 \u1077 \u1090 \u1077 \u1090 \u1100 \'bb).  \
\uc0\u1055 \u1086 \u1089 \u1090 \u1099  \u1085 \u1072  \u1088 \u1091 \u1089 \u1089 \u1082 \u1086 \u1084 , 180\'96280 \u1089 \u1083 \u1086 \u1074 .  \
\uc0\u1057 \u1090 \u1088 \u1091 \u1082 \u1090 \u1091 \u1088 \u1072  \u1082 \u1072 \u1078 \u1076 \u1086 \u1075 \u1086  \u1087 \u1086 \u1089 \u1090 \u1072 :  \
1. \uc0\u55357 \u56613  \u1047 \u1072 \u1075 \u1086 \u1083 \u1086 \u1074 \u1086 \u1082  (\u1093 \u1072 \u1081 \u1087 \u1086 \u1074 \u1099 \u1081 , \u1089  \u1101 \u1084 \u1086 \u1076 \u1079 \u1080 )  \
2. \uc0\u1050 \u1088 \u1072 \u1090 \u1082 \u1086  \u1089 \u1091 \u1090 \u1100  \u1085 \u1086 \u1074 \u1086 \u1089 \u1090 \u1080   \
3. \uc0\u1061 \u1072 \u1081 \u1087  / \u1072 \u1085 \u1072 \u1083 \u1080 \u1079  / \u1089 \u1087 \u1077 \u1082 \u1091 \u1083 \u1103 \u1094 \u1080 \u1103   \
4. 3\'965 \uc0\u1101 \u1084 \u1086 \u1076 \u1079 \u1080  + 2\'963 \u1093 \u1101 \u1096 \u1090 \u1077 \u1075 \u1072   \
5. \uc0\u1042 \u1086 \u1087 \u1088 \u1086 \u1089  \u1082  \u1072 \u1091 \u1076 \u1080 \u1090 \u1086 \u1088 \u1080 \u1080  \u1074  \u1082 \u1086 \u1085 \u1094 \u1077   \
\uc0\u1045 \u1089 \u1083 \u1080  \u1085 \u1086 \u1074 \u1086 \u1089 \u1090 \u1100  \u1090 \u1088 \u1077 \u1073 \u1091 \u1077 \u1090  \u1074 \u1080 \u1079 \u1091 \u1072 \u1083 \u1072  \'97 \u1074  \u1082 \u1086 \u1085 \u1094 \u1077  \u1085 \u1072 \u1087 \u1080 \u1096 \u1080  [IMAGE: \u1082 \u1088 \u1072 \u1090 \u1082 \u1086 \u1077  \u1086 \u1087 \u1080 \u1089 \u1072 \u1085 \u1080 \u1077 ].\
\uc0\u1057 \u1077 \u1081 \u1095 \u1072 \u1089  2026 \u1075 \u1086 \u1076 , \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1081  \u1090 \u1086 \u1083 \u1100 \u1082 \u1086  \u1089 \u1074 \u1077 \u1078 \u1080 \u1077  \u1085 \u1086 \u1074 \u1086 \u1089 \u1090 \u1080 .\
"""\
\
client = AsyncOpenAI(\
    api_key=GROK_API_KEY,\
    base_url="https://api.x.ai/v1"\
)\
\
bot = Bot(token=BOT_TOKEN)\
\
async def post_news():\
    try:\
        response = await client.chat.completions.create(\
            model="grok-4-1-fast-non-reasoning",\
            messages=[\
                \{"role": "system", "content": SYSTEM_PROMPT\},\
                \{"role": "user", "content": "\uc0\u1057 \u1086 \u1073 \u1077 \u1088 \u1080  \u1089 \u1072 \u1084 \u1099 \u1077  \u1075 \u1086 \u1088 \u1103 \u1095 \u1080 \u1077  \u1082 \u1088 \u1080 \u1087 \u1090 \u1086 -\u1085 \u1086 \u1074 \u1086 \u1089 \u1090 \u1080  \u1079 \u1072  \u1087 \u1086 \u1089 \u1083 \u1077 \u1076 \u1085 \u1080 \u1077  6 \u1095 \u1072 \u1089 \u1086 \u1074  \u1080  \u1085 \u1072 \u1087 \u1080 \u1096 \u1080  3\'964 \u1075 \u1086 \u1090 \u1086 \u1074 \u1099 \u1093  \u1087 \u1086 \u1089 \u1090 \u1072  \u1074  \u1089 \u1090 \u1080 \u1083 \u1077  \u1082 \u1072 \u1085 \u1072 \u1083 \u1072  BTC tear."\}\
            ],\
            max_tokens=3000,\
            temperature=0.8\
        )\
        \
        text = response.choices[0].message.content.strip()\
        \
        # \uc0\u1054 \u1090 \u1087 \u1088 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1074  \u1082 \u1072 \u1085 \u1072 \u1083 \
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")\
        print(f"\uc0\u9989  \u1055 \u1086 \u1089 \u1090  \u1086 \u1090 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085  \u1074  \{datetime.now()\}")\
        \
    except Exception as e:\
        print(f"\uc0\u10060  \u1054 \u1096 \u1080 \u1073 \u1082 \u1072 : \{e\}")\
\
async def main():\
    scheduler = AsyncIOScheduler()\
    scheduler.add_job(post_news, 'interval', hours=6, next_run_time=datetime.now())\
    scheduler.start()\
    print("\uc0\u55357 \u56960  \u1041 \u1086 \u1090  \u1079 \u1072 \u1087 \u1091 \u1097 \u1077 \u1085  \u1080  \u1088 \u1072 \u1073 \u1086 \u1090 \u1072 \u1077 \u1090  \u1085 \u1072  \u1072 \u1074 \u1090 \u1086 \u1087 \u1080 \u1083 \u1086 \u1090 \u1077 !")\
    await asyncio.sleep(999999)  # \uc0\u1076 \u1077 \u1088 \u1078 \u1080 \u1084  \u1073 \u1086 \u1090 \u1072  \u1078 \u1080 \u1074 \u1099 \u1084 \
\
if __name__ == "__main__":\
    asyncio.run(main())}