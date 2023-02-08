from initialization.smorest_process import Blueprint

xyzq = Blueprint(
    name="兴业证券",
    import_name=__name__,
    url_prefix="/xyzq",
)


from . import check,research_report_audit,anaplatform, phone, inner_call
