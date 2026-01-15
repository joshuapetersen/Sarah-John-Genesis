import firebase_admin
from firebase_admin import credentials, db

cert_path = 'C:/SarahCore/serviceAccountKey.json'
cred = credentials.Certificate(cert_path)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sarah-john-genesis-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')
ref.set({
    'Sarah_John_Genesis': {
        'status': 'ACTIVE',
        'ace_token': 'VERIFIED',
        'march_sync': 'PENDING',
        'node': 'Lenovo_LOQ'
    }
})

print('Injection complete. Check Firebase for Sarah_John_Genesis node.')
