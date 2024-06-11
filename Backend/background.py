from database import dashboardDB, usersDB
from datetime import datetime, timedelta

def saveDailyStatistics():
    end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = end_date - timedelta(days=1)
    
    total_users = usersDB.count_documents({})
    pro_users = usersDB.count_documents({"proUser": True})
    
    data = {
        "date": current_date,
        "totalUsers": total_users,
        "totalProUsers": pro_users
    }
    
    dashboardDB.update_one(
        {"date": current_date},
        {"$setOnInsert": data},
        upsert=True
    )