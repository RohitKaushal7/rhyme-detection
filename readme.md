# Rhyme Detection

## Up and running

- Start Backend Server `cd server`
  - `virtualenv venv` - create virtual env
  - `source ./venv/bin/activate` - get in the env
  - `pip install -r requirements.txt` - install dependencies
  - `export FLASK_APP=server && export FLASK_ENV=development && flask run` - start server
- Start frontend `cd app`
  - `install dependencies` - pnpm install
  - `pnpm dev` - start server at http://localhost:3000/
