document.addEventListener("DOMContentLoaded", () => {
  const capabilitiesList = document.getElementById("capabilities-list");
  const capabilitySelect = document.getElementById("capability");
  const registerForm = document.getElementById("register-form");
  const messageDiv = document.getElementById("message");

  // Function to display competency matrix in a modal
  async function handleViewMatrix(event) {
    const button = event.target;
    const capability = button.getAttribute("data-capability");

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(capability)}/competency-matrix`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch competency matrix");
      }

      const data = await response.json();
      displayMatrixModal(capability, data.matrix);
    } catch (error) {
      alert("Failed to load competency matrix. Please try again.");
      console.error("Error fetching competency matrix:", error);
    }
  }

  // Function to create and display the matrix modal
  function displayMatrixModal(capabilityName, matrix) {
    // Create modal overlay
    const modalOverlay = document.createElement("div");
    modalOverlay.className = "modal-overlay";

    // Create modal content
    const modalContent = document.createElement("div");
    modalContent.className = "modal-content";

    // Build matrix HTML
    let matrixHTML = `
      <div class="modal-header">
        <h2>${capabilityName} - Competency Matrix</h2>
        <button class="modal-close">&times;</button>
      </div>
      <div class="modal-body">
        <p class="matrix-intro">This competency matrix defines expectations across three key dimensions: Technical Excellence, Client & Delivery Impact, and Team & Practice Leadership.</p>
    `;

    // Iterate through skill levels
    const skillLevels = ["Emerging", "Proficient", "Advanced", "Expert"];
    skillLevels.forEach((level) => {
      if (matrix[level]) {
        matrixHTML += `
          <div class="skill-level-section">
            <h3 class="skill-level-title">${level}</h3>
        `;

        // Technical Excellence
        if (matrix[level].technical_excellence) {
          matrixHTML += `
            <div class="dimension-section">
              <h4 class="dimension-title">🎯 Technical Excellence</h4>
              <ul class="criteria-list">
          `;
          Object.entries(matrix[level].technical_excellence).forEach(
            ([key, value]) => {
              matrixHTML += `<li><strong>${formatKey(key)}:</strong> ${value}</li>`;
            }
          );
          matrixHTML += `</ul></div>`;
        }

        // Client & Delivery Impact
        if (matrix[level].client_delivery) {
          matrixHTML += `
            <div class="dimension-section">
              <h4 class="dimension-title">🤝 Client & Delivery Impact</h4>
              <ul class="criteria-list">
          `;
          Object.entries(matrix[level].client_delivery).forEach(
            ([key, value]) => {
              matrixHTML += `<li><strong>${formatKey(key)}:</strong> ${value}</li>`;
            }
          );
          matrixHTML += `</ul></div>`;
        }

        // Team & Practice Leadership
        if (matrix[level].leadership) {
          matrixHTML += `
            <div class="dimension-section">
              <h4 class="dimension-title">👥 Team & Practice Leadership</h4>
              <ul class="criteria-list">
          `;
          Object.entries(matrix[level].leadership).forEach(([key, value]) => {
            matrixHTML += `<li><strong>${formatKey(key)}:</strong> ${value}</li>`;
          });
          matrixHTML += `</ul></div>`;
        }

        matrixHTML += `</div>`; // Close skill-level-section
      }
    });

    matrixHTML += `</div>`; // Close modal-body

    modalContent.innerHTML = matrixHTML;
    modalOverlay.appendChild(modalContent);
    document.body.appendChild(modalOverlay);

    // Add event listener to close button
    const closeBtn = modalContent.querySelector(".modal-close");
    closeBtn.addEventListener("click", () => {
      document.body.removeChild(modalOverlay);
    });

    // Close on overlay click
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) {
        document.body.removeChild(modalOverlay);
      }
    });
  }

  // Helper function to format keys
  function formatKey(key) {
    return key
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  // Function to fetch capabilities from API
  async function fetchCapabilities() {
    try {
      const response = await fetch("/capabilities");
      const capabilities = await response.json();

      // Clear loading message
      capabilitiesList.innerHTML = "";

      // Populate capabilities list
      Object.entries(capabilities).forEach(([name, details]) => {
        const capabilityCard = document.createElement("div");
        capabilityCard.className = "capability-card";

        const availableCapacity = details.capacity || 0;
        const currentConsultants = details.consultants ? details.consultants.length : 0;

        // Create consultants HTML with delete icons
        const consultantsHTML =
          details.consultants && details.consultants.length > 0
            ? `<div class="consultants-section">
              <h5>Registered Consultants:</h5>
              <ul class="consultants-list">
                ${details.consultants
                  .map(
                    (email) =>
                      `<li><span class="consultant-email">${email}</span><button class="delete-btn" data-capability="${name}" data-email="${email}">❌</button></li>`
                  )
                  .join("")}
              </ul>
            </div>`
            : `<p><em>No consultants registered yet</em></p>`;

        const competencyMatrixButton = details.has_competency_matrix
          ? `<button class="view-matrix-btn" data-capability="${name}">📋 View Competency Matrix</button>`
          : '';

        capabilityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Practice Area:</strong> ${details.practice_area}</p>
          <p><strong>Industry Verticals:</strong> ${details.industry_verticals ? details.industry_verticals.join(', ') : 'Not specified'}</p>
          <p><strong>Capacity:</strong> ${availableCapacity} hours/week available</p>
          <p><strong>Current Team:</strong> ${currentConsultants} consultants</p>
          ${competencyMatrixButton}
          <div class="consultants-container">
            ${consultantsHTML}
          </div>
        `;

        capabilitiesList.appendChild(capabilityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        capabilitySelect.appendChild(option);
      });

      // Add event listeners to delete buttons
      document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", handleUnregister);
      });

      // Add event listeners to view matrix buttons
      document.querySelectorAll(".view-matrix-btn").forEach((button) => {
        button.addEventListener("click", handleViewMatrix);
      });
    } catch (error) {
      capabilitiesList.innerHTML =
        "<p>Failed to load capabilities. Please try again later.</p>";
      console.error("Error fetching capabilities:", error);
    }
  }

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const capability = button.getAttribute("data-capability");
    const email = button.getAttribute("data-email");

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(
          capability
        )}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";

        // Refresh capabilities list to show updated consultants
        fetchCapabilities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to unregister. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error unregistering:", error);
    }
  }

  // Handle form submission
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const capability = document.getElementById("capability").value;

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(
          capability
        )}/register?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        registerForm.reset();

        // Refresh capabilities list to show updated consultants
        fetchCapabilities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to register. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error registering:", error);
    }
  });

  // Initialize app
  fetchCapabilities();
});
