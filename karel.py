# insert correct credentials into 10 config lines below
# run this script with python3 karel.py
# invite MATRIX-LOGIN to matrix #ROOM of Your choice 
# after any user in #ROOM writes !txt2img "prompt" picture will be generated, stored in the webpage repository and link to it will be provided in #ROOM
# more (parametrized prompts, integration with Kastalia KMS etc.) to come soon

api_host='AUTOMATIC1111-HOST'
api_port='7860'
api_login='AUTOMATIC1111-LOGIN'
api_pass='AUTOMATIC1111-PASS'
local_dir="/var/www/YOURPROJECTLOCALDIR"
url_prefix="https://YOURPROJECTDOMAIN"
m3x_homeserver="https://MATRIXHOMESERVER"
m3x_login="MATRIX-LOGIN"
m3x_pass="MATRIX-PASS"
PREFIX = '!'

import os
try:
    os.remove('session.txt')
except:
    1
import simplematrixbotlib as botlib
import webuiapi

creds = botlib.Creds(m3x_homeserver, m3x_login, m3x_pass)
# create API client
api = webuiapi.WebUIApi(host=api_host, port=api_port, use_https=True)
api.set_auth(api_login,api_pass)
#activate Matrix bot
bot = botlib.Bot(creds)

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("txt2img"):
        prompt=" ".join(arg for arg in match.args())
        print("PROMPTED WITH "+prompt)
        result1 = api.txt2img(prompt=prompt,negative_prompt="",seed=1003,styles=["anime"], sampler_index='DDIM', steps=30, enable_hr=True, hr_scale=2, hr_upscaler=webuiapi.HiResUpscaler.Latent, hr_second_pass_steps=20, hr_resize_x=512, hr_resize_y=512, denoising_strength=0.4)
        fname=prompt.replace(" ","_")+".png"
        output_file=local_dir+fname
        print(output_file+" GENERATED")
        result1.image.save(output_file)
        await bot.api.send_text_message(
            room.room_id, url_prefix+fname
        )
bot.run()
