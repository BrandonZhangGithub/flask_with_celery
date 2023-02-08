from . import app


@app.route("/health_check")
def health_check():
    """如果需要做额外的检查请修改本接口"""
    return ""
