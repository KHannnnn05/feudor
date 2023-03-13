import uvicorn
from config import app
import handlers


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')