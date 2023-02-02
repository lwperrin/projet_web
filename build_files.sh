# build_files.sh
pip install -r requirements.txt
python3.9 source/manage.py collectstatic --noinput