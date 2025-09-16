// Copyright (c) 2025 Lejla Husić
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

(function () {
  var width, height, largeHeader, canvas, ctx, points, target, animateHeader = true;

  // Initialize canvas and animation
  initHeader();
  initAnimation();
  addListeners();

  /**
   * Initializes the canvas header and generates animated points.
   */
  function initHeader() {
    width = window.innerWidth;
    height = window.innerHeight;
    target = { x: width / 2, y: height / 2 };

    largeHeader = document.getElementById("large-header");
    largeHeader.style.height = height + "px";

    canvas = document.getElementById("demo-canvas");
    canvas.width = width;
    canvas.height = height;
    ctx = canvas.getContext("2d");

    // Generate grid of points
    points = [];
    for (var x = 0; x < width; x += width / 20) {
      for (var y = 0; y < height; y += height / 20) {
        var px = x + (Math.random() * width) / 20;
        var py = y + (Math.random() * height) / 20;
        points.push({ x: px, originX: px, y: py, originY: py });
      }
    }

    // Find 5 closest neighbors for each point
    for (var i = 0; i < points.length; i++) {
      var closest = [];
      var p1 = points[i];
      for (var j = 0; j < points.length; j++) {
        var p2 = points[j];
        if (p1 !== p2) {
          for (var k = 0; k < 5; k++) {
            if (!closest[k] || getDistance(p1, p2) < getDistance(p1, closest[k])) {
              closest[k] = p2;
              break;
            }
          }
        }
      }
      p1.closest = closest;
    }

    // Assign circles to each point
    for (var i in points) {
      points[i].circle = new Circle(points[i], 2 + Math.random() * 2, "rgba(255,255,255,0.3)");
    }
  }

  /**
   * Adds mouse and window event listeners.
   */
  function addListeners() {
    if (!("ontouchstart" in window)) {
      window.addEventListener("mousemove", mouseMove);
    }
    window.addEventListener("scroll", scrollCheck);
    window.addEventListener("resize", resize);
  }

  /**
   * Updates target position based on mouse movement.
   * @param {MouseEvent} e
   */
  function mouseMove(e) {
    var posx = e.pageX || e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
    var posy = e.pageY || e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    target.x = posx;
    target.y = posy;
  }

  /**
   * Toggles animation based on scroll position.
   */
  function scrollCheck() {
    animateHeader = document.body.scrollTop <= height;
  }

  /**
   * Resizes canvas and header on window resize.
   */
  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    largeHeader.style.height = height + "px";
    canvas.width = width;
    canvas.height = height;
  }

  /**
   * Starts the animation loop and shifts points.
   */
  function initAnimation() {
    animate();
    for (var i in points) {
      shiftPoint(points[i]);
    }
  }

  /**
   * Animates canvas frame-by-frame.
   */
  function animate() {
    if (animateHeader) {
      ctx.clearRect(0, 0, width, height);
      for (var i in points) {
        var dist = getDistance(target, points[i]);
        points[i].active = dist < 4000 ? 0.3 : dist < 20000 ? 0.1 : dist < 40000 ? 0.02 : 0;
        points[i].circle.active = points[i].active * 2;
        drawLines(points[i]);
        points[i].circle.draw();
      }
    }
    requestAnimationFrame(animate);
  }

  /**
   * Randomly shifts a point's position with easing.
   * @param {Object} p
   */
  function shiftPoint(p) {
    TweenLite.to(p, 1 + Math.random(), {
      x: p.originX - 50 + Math.random() * 100,
      y: p.originY - 50 + Math.random() * 100,
      ease: Circ.easeInOut,
      onComplete: function () {
        shiftPoint(p);
      },
    });
  }

  /**
   * Draws lines between a point and its closest neighbors.
   * @param {Object} p
   */
  function drawLines(p) {
    if (!p.active) return;
    for (var i in p.closest) {
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(p.closest[i].x, p.closest[i].y);
      ctx.strokeStyle = "rgba(209, 207, 54," + p.active + ")";
      ctx.stroke();
    }
  }

  /**
   * Circle constructor for animated points.
   * @param {Object} pos
   * @param {number} rad
   * @param {string} color
   */
  function Circle(pos, rad, color) {
    var _this = this;
    (function () {
      _this.pos = pos;
      _this.radius = rad;
      _this.color = color;
    })();

    /**
     * Draws the circle on canvas.
     */
    this.draw = function () {
      if (!_this.active) return;
      ctx.beginPath();
      ctx.arc(_this.pos.x, _this.pos.y, _this.radius, 0, 2 * Math.PI, false);
      ctx.fillStyle = "rgba(156,217,249," + _this.active + ")";
      ctx.fill();
    };
  }

  /**
   * Calculates squared distance between two points.
   * @param {Object} p1
   * @param {Object} p2
   * @returns {number}
   */
  function getDistance(p1, p2) {
    return Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2);
  }
})();

// DOM elements
const button = document.querySelector(".btn");
const fileInput = document.getElementById("csv-input");

// Trigger file picker on button click
button.addEventListener("click", () => {
  fileInput.click();
});

// Upload file when selected
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);
  $("#loadingOverlay").show();

  fetch("/upload-csv", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("CSV uploaded:", data);
      alert("CSV uploaded successfully!");
    })
    .catch((error) => {
      console.error("Upload failed:", error);
      alert("Upload failed.");
    })
    .finally(() => $("#loadingOverlay").hide());
});

const openPopup = document.getElementById("openPopupCostumers");
const closePopup1 = document.getElementById("closePopup1");
const closePopup2 = document.getElementById("closePopup2");
const popup = document.getElementById("costumerInformationPopup");
const popup2 = document.getElementById("popupCostumersAndElBills");
const openPopup2 = document.getElementById("openPopupCostumersAndElBills");

// Show popups
openPopup.addEventListener("click", () => popup.style.display = "flex");
openPopup2.addEventListener("click", () => popup2.style.display = "flex");

// Hide popups
closePopup1.addEventListener("click", () => popup.style.display = "none");
closePopup2.addEventListener("click", () => popup2.style.display = "none");

/**
 * Loads billing data into the DataTable.
 */
function loadBills() {
  let table = $("#billTable").DataTable({
    processing: true,
    ajax: { url: "/get-bills", type: "GET", dataSrc: "" },
    columns: [
      { data: "name" },
      { data: "email" },
      { data: "costumer_id" },
      {
        data: "billing_month",
        render: function (data, type, row) {
          const date = new Date(data);
          const month = date.toLocaleString("en-US", { month: "long" });
          const year = date.getFullYear();
          return `${month} ${year}`;
        },
      },
      {
        data: "billing_value",
        render: function (data, type, row) {
          return parseFloat(data).toFixed(2) + " €";
        },
      },
      {
        data: "billing_consumption",

        render: function (data, type, row) {
          return parseFloat(data).toFixed(2);
        },
      },
      {
        data: null,
        orderable: false,
        render: function (data, type, row) {
          return `<button class="btn btn-sm btn-primary view-btn" style="width:100px;background-color:#000;color:#fff"data-id="${row.costumer_id}">View</button>`;
        },
      },
    ],
    dom: "rBtipf",
    paging: false,
    deferRender: true,
    bDestroy: true,
  });
}

$("#billTable").on("click", ".view-btn", function () {
  const rowData = $("#billTable").DataTable().row($(this).closest("tr")).data();

  const customerId = rowData.costumer_id;
  const billingMonth = new Date(rowData.billing_month);
  const monthStr = billingMonth.toISOString().slice(0, 7); // "2024-08"
  $("#loadingOverlay").show();
  fetch("/render-file", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(rowData),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Failed to generate file");
      return response.blob();
    })
    .then((blob) => {
      const filename = `bill_report-${customerId}_${monthStr}.pdf`; // or .txt/.csv
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    })
    .catch((error) => {
      console.error("Error generating report:", error);
    })
    .finally(() => $("#loadingOverlay").hide());
});
