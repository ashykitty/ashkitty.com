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

async function spooky()
{
	const banner = document.getElementsByClassName("banner")[0];
	banner.src = "static/spooky.gif";
	
	const background = document.getElementsByClassName("background")[0];
	background.background_image = "#000000FF";
	
}
