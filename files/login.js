async function login()
{
	const key = document.getElementById("key_txt");	
	const res = await fetch("/auth",
		{
			method: "post",
			body: key.value
		}
	);
	var ret = await res.text();
	if(ret === "wrong lol")
	{
		window.location.href = "https://ashkitty.com/wrong";
	} else {
		document.cookie = ret;
		window.location.href = "https://ashkitty.com/correct";
	}
}

document.getElementById("login_btn").addEventListener('click', login)
