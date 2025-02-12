$env:PGPASSWORD = 'root'
dropdb -U postgres stockchartstic --force
createdb -U postgres stockchartstic