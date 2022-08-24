echo "DEBUG=$DEBUG" > .env
echo "SECRET_KEY=$SECRET_KEY" >> .env
echo "ALGORITHM=$ALGORITHM" >> .env
echo "ALLOWED_HOSTS=$ALLOWED_HOSTS" >> .env
echo "DB_NAME=$DB_NAME" >> .env
echo "DB_USER=$DB_USER" >> .env
echo "DB_PASSWORD=$DB_PASSWORD" >> .env
echo "DB_HOST=$DB_HOST" >> .env
echo "DB_PORT=$DB_PORT" >> .env
echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> .env
echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env
echo "AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME" >> .env
echo "AWS_REGION=$AWS_REGION" >> .env

cat .env

gunicorn --bind 0.0.0.0:8000 review_king.wsgi:application