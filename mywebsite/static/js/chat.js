document.addEventListener("DOMContentLoaded", function () {
	var user = "{{ request.user }}";
	var room_id = "{{ room.id }}";
  
	var userList = document.getElementById("userList");
  
	function addUser(username) {
	  var li = document.createElement("li");
	  li.className = "list-group-item";
	  if (username === user) {
		li.classList.add("list-group-item-success");
	  }
	  li.textContent = username;
	  userList.appendChild(li);
	}
  
	function removeUser(username) {
	  var items = userList.getElementsByTagName("li");
	  for (var i = 0; i < items.length; i++) {
		if (items[i].textContent === username) {
		  userList.removeChild(items[i]);
		  break;
		}
	  }
	}
  
	var chatSocket = new WebSocket(
	  "ws://" + window.location.host + "/ws/room/" + room_id + "/",
	);
  
	chatSocket.onmessage = function (e) {
	  var data = JSON.parse(e.data);
	  if (data.type === "user_join") {
		addUser(data.username);
	  } else if (data.type === "user_leave") {
		removeUser(data.username);
	  }
	};
  
	chatSocket.onclose = function (e) {
	  console.error("Chat socket closed unexpectedly");
	};
  });