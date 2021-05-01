import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate(
    "E:\\certificates\\tasker\\tasker_service_account_key.json")
# cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'todo-8e2e1',
})

db_firestore = firestore.client()


# Add data

# doc_ref = db.collection('jwt_tokens').document('alovelace')
# doc_ref.set({
#     'first': 'Ada',
#     'last': 'Lovelace',
#     'born': 1815
# })


# Fetch data

# users_ref = db_firestore.collection('jwt_tokens')
# docs = users_ref.stream()

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')
