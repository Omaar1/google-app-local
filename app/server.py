from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO
import logging
import os


from fastai import *
from fastai.vision import *

classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
path = Path(__file__).parent


#export_file_url = 'https://drive.google.com/uc?export=download&id=1smQEO1X_xXpJfxGOaVR0n7PQEmkucuPi'
export_file_name = 'trained_model_fbeta95.pkl'

path = Path(__file__).parent
files = os.listdir()
print(os.listdir())


app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))



### Downloading the trained model

#async def download_file(url, dest):
#    if dest.exists(): return
#    async with aiohttp.ClientSession() as session:
 #       async with session.get(url) as response:
  #          data = await response.read()
   #         with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    #await download_file(export_file_url, path/export_file_name)
	path='./app/models'
	print(path+'++++')
	try:
		learn = load_learner(path, export_file_name)
		return learn
	except RuntimeError as e:
		if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
			print(e)
			message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
			raise RuntimeError(message)
		else:
			raise
#
#
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()



@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    logging.info('*******This  is   start*******')
    return HTMLResponse(html.open().read())



@app.route('/analyze', methods=['POST'])
async def analyze(request):
    logging.info('*******This is an info message*******')
    logging.info(request)
    data = await request.form()
    logging.error('*******!!!startAnalyze!!!********')
    # logging.info(data)
	
    try:
        img_bytes = await (data['file'].read())
        img = open_image(BytesIO(img_bytes))
        prediction = learn.predict(img)
    except AttributeError as error:
        # Output expected AttributeErrors.
        logging.error(str(error))
	
	


    prediction = learn.predict(img)
    p1 = prediction[0]
    p2 = prediction[2].numpy().tolist()
    strp2 = ','.join(str(e) for e in p2)
    return JSONResponse({'result': str(p1) , 'conf':strp2 })

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app, host='0.0.0.0', port=8080)
