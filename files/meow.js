async function meow( encode)
{
	const box = document.getElementById("meow_text");	
	const res = await fetch("/meow",
		{
			method: "get",
			body: encode+':'+box.value
		}
	);
	box.value = await res.text();
}

