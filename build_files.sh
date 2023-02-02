# build_files.sh
sudo apt-get install libsqlite3-dev libsqlite3
pip install -r requirements.txt
python3.9 source/manage.py collectstatic --noinput