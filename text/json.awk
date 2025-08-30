#
# Extract a JSON value in an object:
#
# items = get_json_value(json, "payload.tree.items")
#
# Or in an array:
#
# while ((item = get_json_value(items, i++)))
# 	name = decode_json_string(get_json_value(item, "name"))
#
# Or both:
#
# item = get_json_value(json, "payload.tree.items.0")
#
function get_json_value(s, key, type, all, rest, isval, i, c, j, k) {
	type = substr(s, 1, 1)
	if (type != "{" && type != "[") error("invalid json array/object " s)
	all = key == "" && key == 0
	if (!all && (j = index(key, "."))) {
		rest = substr(key, j+1)
		key = substr(key, 1, j-1)
	}
	if (type == "[") k = 0
	isval = type == "["
	for (i = 2; i < length(s); i += length(c)) {
		c = substr(s, i, 1)
		if (c == "\"") {
			if (!match(substr(s, i), /^"(\\.|[^\\"])*"/))
				error("invalid json string " substr(s, i))
			c = substr(s, i, RLENGTH)
			if (!isval) k = substr(c, 2, length(c)-2)
		}
		else if (c == "{" || c == "[") {
			c = (!all && k == key && !(rest == "" && rest == 0)) ? \
				get_json_value(substr(s, i), rest) : \
				get_json_value(substr(s, i))
		}
		else if (c == "}" || c == "]") break
		else if (c == ",") isval = type == "["
		else if (c == ":") ;
		else if (c ~ /[[:space:]]/) continue
		else {
			if (!match(substr(s, i), /[]},[:space:]]/))
				error("invalid json value " substr(s, i))
			c = substr(s, i, RSTART-1)
		}
		if (!all && isval && k == key) return c
		if (type == "{" && c == ":") isval = 1
		if (type == "[" && c == ",") ++k
	}
	if (all) return substr(s, 1, i)
}

function decode_json_string(s) {
	# Does not handle unicode escape sequences
	if (s !~ /^"/ || s ~ /\\u/)
		error("cannot handle JSON string " s)
	s = substr(s, 2, length(s)-2)
	gsub(/\\b/, "\b", s)
	gsub(/\\f/, "\f", s)
	gsub(/\\n/, "\n", s)
	gsub(/\\r/, "\r", s)
	gsub(/\\t/, "\t", s)
	gsub(/\\"/, "\"", s)
	gsub(/\\\//, "/", s)
	gsub(/\\\\/, "\\", s)
	return s
}

function error(msg) {
	printf "%s: %s\n", ARGV[0], msg > "/dev/stderr"
	exit 1
}

#
# Example usage
#
# $ curl https://httpbin.org/json | awk -f json.awk slideshow.title
# "Sample Slide Show"
#
BEGIN {
	while (ret = getline l < "/dev/stdin") {
		if (ret == -1) error("getline error")
		s = s l
	}
	print get_json_value(s, ARGV[1])
}
