from models import Post

def best_product_id() -> int:
    result = Post.select(Post.likes, Post.comments)
    max_id = 0
    max_summ = 0
    for record in result:
        if record.likes + record.comments > max_summ:
            max_summ = record.likes + record.comments
            max_id = record.id
    return max_id
