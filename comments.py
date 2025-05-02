import db

def create_comment(user_id, comment):
    sql = "INSERT INTO comments (user_id, comment) VALUES (?, ?)"
    db.execute(sql, [user_id, comment])

def get_comments():
    sql = "SELECT c.comment, u.username FROM comments c JOIN users u ON c.user_id = u.id"
    result = db.query(sql)
    return result