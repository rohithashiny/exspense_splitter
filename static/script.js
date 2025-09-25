document.addEventListener("DOMContentLoaded", () => {
  // Handle Signup
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = {
        name: signupForm.name.value,
        email: signupForm.email.value,
        password: signupForm.password.value
      };

      try {
        const res = await fetch("/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });

        const data = await res.json();

        if (res.ok) {
          alert("✅ Signup successful! Please login now.");
          window.location.href = "/login-page";
        } else {
          alert("❌ Error: " + data.error);
        }
      } catch (err) {
        console.error("Signup failed:", err);
        alert("Something went wrong, try again.");
      }
    });
  }

  // Handle Login
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = {
        email: loginForm.email.value,
        password: loginForm.password.value
      };

      try {
        const res = await fetch("/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });

        const data = await res.json();

        if (res.ok) {
          alert("✅ Login successful!");
          window.location.href = "/dashboard"; 
        } else {
          alert("❌ Error: " + data.error);
        }
      } catch (err) {
        console.error("Login failed:", err);
        alert("Something went wrong, try again.");
      }
    });
  }

  // Load users
  async function loadUsers() {
    try {
      const res = await fetch("/users");
      const users = await res.json();

      const paidBySelect = document.getElementById("paidBy");
      const participantsDiv = document.getElementById("participantsList");

      if (paidBySelect) {
        paidBySelect.innerHTML = "";
        users.forEach(user => {
          const option = document.createElement("option");
          option.value = user.name;   // use name
          option.textContent = user.name;
          paidBySelect.appendChild(option);
        });
      }

      if (participantsDiv) {
        participantsDiv.innerHTML = "";
        users.forEach(user => {
          const label = document.createElement("label");
          const checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.value = user.name;  // use name
          label.appendChild(checkbox);
          label.append(" " + user.name);
          participantsDiv.appendChild(label);
          participantsDiv.appendChild(document.createElement("br"));
        });
      }
    } catch (err) {
      console.error("Error loading users:", err);
    }
  }

  // Handle Expense
  const expenseForm = document.getElementById("expenseForm");
  if (expenseForm) {
    expenseForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const amount = expenseForm.amount.value;
      const description = expenseForm.description.value;
      const paid_by = document.getElementById("paidBy").value;

      const participantNames = Array.from(
        document.querySelectorAll("#participantsList input:checked")
      ).map(cb => cb.value);

      try {
        const res = await fetch("/expenses", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            amount,
            description,
            paid_by,
            participants: participantNames
          })
        });

        const data = await res.json();
        if (res.ok) {
          alert("✅ Expense added successfully");
        } else {
          alert("❌ Error: " + data.error);
        }
      } catch (err) {
        console.error("Error adding expense:", err);
        alert("Something went wrong.");
      }
    });
  }

  // Fetch Balances
  async function fetchBalances() {
    try {
      const res = await fetch("/balances");
      const data = await res.json();
      document.getElementById("balancesOutput").textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      console.error("Error fetching balances:", err);
    }
  }

  // Fetch Settlements
  async function fetchSettlements() {
    try {
      const res = await fetch("/settlements");
      const data = await res.json();
      document.getElementById("settlementsOutput").textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      console.error("Error fetching settlements:", err);
    }
  }

  // Logout
  window.logout = function() {
    window.location.href = "/login-page";
  }

  // Auto load on dashboard
  if (window.location.pathname === "/dashboard") {
    loadUsers();
    fetchBalances();
    fetchSettlements();
  }
});
