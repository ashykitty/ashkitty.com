async function meow()
{
	const box = document.getElementById("meow_text");	
	const res = await fetch("/meow",
		{
			method: "post",
			body: box.value
		}
	);
	box.value = await res.text();
}

document.getElementById("meow_btn").addEventListener('click', meow)
