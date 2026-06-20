import sys
import io
import ast
import traceback


def execute_python_safe(code: str, globals_dict: dict = None) -> dict:
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ("open", "exec", "eval", "__import__", "system", "popen"):
                    return {"error": f"Forbidden function: {node.func.attr}"}
            elif isinstance(node.func, ast.Name):
                if node.func.id in ("exec", "eval", "open", "__import__"):
                    return {"error": f"Forbidden function: {node.func.id}"}

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    result_dict = {"result": None, "error": None}

    try:
        safe_globals = {
            "pd": __import__("pandas", fromlist=["DataFrame"]),
            "print": lambda *args, **kwargs: print(*args, **kwargs),
            "__builtins__": {
                "print": print,
                "len": len,
                "range": range,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "min": min,
                "max": max,
                "sum": sum,
                "abs": abs,
                "round": round,
                "True": True,
                "False": False,
                "None": None,
            },
        }
        if globals_dict:
            safe_globals.update(globals_dict)

        exec(code, safe_globals)
        output = sys.stdout.getvalue()
        result_dict["output"] = output
    except Exception:
        result_dict["error"] = traceback.format_exc()
    finally:
        sys.stdout = old_stdout

    return result_dict
