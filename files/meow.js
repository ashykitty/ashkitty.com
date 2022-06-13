async function meow( encode)
{
	const box = document.getElementById("meow_text");	
	const res = await fetch("/meow",
		{
			method: "post",
			body: encode+':'+box.value
		}
	);
	box.value = await res.text();
}

document.getElementById("encode_btn").addEventListener('click', function(){meow(true)})
document.getElementById("decode_btn").addEventListener('click', function(){meow(false)})
