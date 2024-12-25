document.getElementById("logout-btn").addEventListener("click", function () {
    Swal.fire({
      title: "Are you sure?",
      text: "You will be logged out.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, log me out!",
      cancelButtonText: "No, stay here",
    }).then((result) => {
      if (result.isConfirmed) {
        // Perform logout action (redirect to logout endpoint or clear session)
        window.location.href = "/logout"; // Replace with your logout URL
      } else {
        // Optionally show a message for staying on the site
        Swal.fire({
          title: "Cancelled",
          text: "You are still logged in.",
          icon: "info",
        });
      }
    });
  });
  