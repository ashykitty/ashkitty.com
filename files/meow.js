async function meow(encode)
{
	const box = document.getElementById("meow_text");	
	const res = await fetch("/meow/",
		{
			method: "post",
			headers:{'Content-Type':'application/json'},
			body: JSON.stringify({encode:encode,msg:box.value})
		}
	);
	box.value = await res.json();
}

