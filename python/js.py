import js2py

# &#xcd5b;&#xca92;&#xcd85;&#xcb86;&#xcab7;&#xcbe8;
js_code = """
function Add(x, y) {
    return x + y;
}
"""

js_add = js2py.eval_js(js_code)

if __name__ == "__main__":
    print(js_add(1, 3))
