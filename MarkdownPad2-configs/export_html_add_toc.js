
<script type = "text/javascript" > 
document.addEventListener("DOMContentLoaded", function()
{
	var div1			= document.createElement("div");
	div1.style.cssText	= "clear:both";

	// create TOC list
	var outline 		= document.createElement("div");
	outline.setAttribute("id", "outline-list");
	outline.style.cssText = "border:solid 1px #ccc; background:#eee; min-width:200px;padding:4px 10px;";

	var ele_p			= document.createElement("p");
	ele_p.style.cssText = "text-align: left; margin: 0;";
	outline.appendChild(ele_p);

	var ele_span		= document.createElement("span");

	// ele_span.style.cssText = "float: left;";
	var ele_text		= document.createTextNode("TOC");
	ele_span.appendChild(ele_text);

	var ele_a			= document.createElement("a");
	ele_a.appendChild(document.createTextNode("[+]"));
	ele_a.setAttribute("href", "#");
	ele_a.setAttribute("onclick", "javascript:return openct(this);");
	ele_a.setAttribute("title", "Click to Open TOC");

	ele_span.appendChild(ele_a);
	ele_p.appendChild(ele_span);

	var ul_top			= document.createElement("ul"); // 顶级
	ul_top.style.cssText = "display:none;margin-left:14px;padding-left:14px;line-height:160%;";
	ul_top.setAttribute("id", "outline_ol");
	outline.appendChild(ul_top);
	var div1			= document.createElement("div");
	div1.style.cssText	= "clear:both";

	document.body.insertBefore(outline, document.body.childNodes[0]);

	// get all the headlines
	var headers 		= document.querySelectorAll('h1,h2,h3,h4,h5,h6');

	if (headers.length < 2)
		return;


	var old_h = 1;

	var ul_array = new Array(7);
	var ul_current = null;
	ul_array[1] = ul_top;

	for (var i = 0; i < headers.length; i++)
	{
		// get H* and prepare for the ordered list 
		var header = headers[i];

		//header.setAttribute("id", "t" + i + header.tagName);
		header.setAttribute("id", header.textContent);
		var h = parseInt(header.tagName.substr(1), 10);

		// assert  1<=h && h <= 6
		
		ul_current = 0;
		if (h < old_h)
		{
			for (var j = h+1; j <= 6; j++)
			{
				ul_array[j] = null;
			}
			ul_current = h;
		}
		else if (h == old_h)
		{
			ul_current = h;
		}
		else if (h > old_h)
		{
			ul_current = old_h + 1; /* 是old_h + 1的原因： h如果是old_h + 2 或者 + 3时，
										我们依然按 + 1来做 */
		}
		
		if (ul_array[ul_current] == null)
		{
			ul_array[ul_current] = document.createElement("ul");
			if (h>1)
			{
				ul_array[h-1].lastChild.appendChild(ul_array[ul_current]);
			}
		}

		var elem_li = document.createElement("li");
		ul_array[ul_current].appendChild(elem_li);
		
		var a = document.createElement("a");

		// set href for the TOC item 
		//a.setAttribute("href", "#t" + i + header.tagName);
		a.setAttribute("href", "#" + header.textContent);

		// TOC item text
		a.innerHTML  = "h" + h + header.textContent;


		elem_li.appendChild(a);

		old_h = h;
	}

}


);

// 
function openct(e)
{
	if (e.innerHTML == '[+]')
	{
		// createTextNode
		e.setAttribute('title', 'collapse');
		e.innerHTML 		= '[-]';
		var 			element = document.getElementById("outline_ol");

		element.style.cssText = "margin-left:14px;padding-left:14px;line-height:160%;";
	}
	else 
	{
		e.setAttribute('title', 'expand');
		e.innerHTML 		= '[+]';
		var 			element = document.getElementById("outline_ol");

		element.style.cssText = "display:none;margin-left:14px;padding-left:14px;line-height:160%;";
	}

	e.blur();
	return false;
}


</script>
