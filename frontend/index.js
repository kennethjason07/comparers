window.onload = function() {
    document.querySelector('.login-container').style.display = 'block';
    document.querySelector('.main').style.display = 'none'; // Ensure main content is hidden initially
}


function authenticateUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Set your desired username and password
    const validUsername = "admin";
    const validPassword = "password123";

    // Simple check for username and password
    if (username === validUsername && password === validPassword) {
        // Redirect to a different page (e.g., "dashboard.html")
        window.location.href = 'index.html'; // Change this to your desired page
    } else {
        alert("Invalid username or password. Please try again.");
    }
}


// Function to show content based on clicked tab
function showContent(id) {
    // Hide all content sections
    const contentSections = document.querySelectorAll('.content-main > div');
    contentSections.forEach(section => {
        if (section.id === id) {
            section.classList.remove('hidden'); // Show the clicked section
        } else {
            section.classList.add('hidden'); // Hide other sections
        }
    });

}

function formatDateTime(dateTimeString) {
    // Create a Date object from the string
    const date = new Date(dateTimeString);
    
    // Extract date in YYYY-MM-DD format
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(date.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
}

function calculateTotals() {
    // Get quantity and amount input values
    const suitQty = parseFloat(document.getElementById('suit_qty').value) || 0;
    const suitAmt = parseFloat(document.getElementById('suit_amount').value) || 0;

    const safariQty = parseFloat(document.getElementById('safari_qty').value) || 0;
    const safariAmt = parseFloat(document.getElementById('safari_amount').value) || 0;

    const pantQty = parseFloat(document.getElementById('pant_qty').value) || 0;
    const pantAmt = parseFloat(document.getElementById('pant_amount').value) || 0;

    const shirtQty = parseFloat(document.getElementById('shirt_qty').value) || 0;
    const shirtAmt = parseFloat(document.getElementById('shirt_amount').value) || 0;

    // Calculate total quantities and total amount
    const totalQty = suitQty + safariQty + pantQty + shirtQty;
    const totalAmt = suitAmt + safariAmt + pantAmt + shirtAmt;

    // Update the total quantity and amount in the respective fields
    document.getElementById('total_qty').value = totalQty;
    document.getElementById('total_amt').value = totalAmt.toFixed(2);
}



function toggleMeasurements() {
    console.log("toggleMeasurements function called");

    var pantSection = document.getElementById("pant-section");
    var shirtSection = document.getElementById("shirt-section");
    var extraSection = document.getElementById("extra-section");

    // Get all checkboxes for measurements selection
    var selectedValues = document.querySelectorAll('input[name="measurements-selection"]:checked');
    
    console.log("Selected values:", selectedValues); // Check selected values in the console

    // Hide all sections initially
    pantSection.classList.add("hidden");
    shirtSection.classList.add("hidden");
    extraSection.classList.add("hidden");

    // Show sections based on selected checkboxes
    selectedValues.forEach(selection => {
        console.log("Processing selection:", selection.value); // Check which values are being processed
        if (selection.value === "pant") {
            pantSection.classList.remove("hidden");
        } else if (selection.value === "shirt") {
            shirtSection.classList.remove("hidden");
        } else if (selection.value === "extra") {
            extraSection.classList.remove("hidden");
        }
    });
}


document.getElementById('new-bill-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission behavior
    
    const customerName = document.getElementById("customer-name").value;
    const mobileNo = document.getElementById("mobile-number").value;
    const dateIssue = document.getElementById("date_issue").value;
    const deliveryDate = document.getElementById("delivery-date").value;
    const garmentType = document.getElementById("garment_type").value;
    const suitQty = document.getElementById("suit_qty").value;
    const safariQty = document.getElementById("safari_qty").value;
    const pantQty = document.getElementById("pant_qty").value;
    const shirtQty = document.getElementById("shirt_qty").value;
    const totalQty = document.getElementById("total_qty").value;
    const todayDate = document.getElementById("today-date").value;
    const dueDate = document.getElementById("due-date").value;
    const totalAmt = document.getElementById("total_amt").value;
    const paymentMode = document.getElementById("Payment").value;
    const paymentStatus = document.getElementById("payementstatus").value;
    const paymentAmount = document.getElementById("total_amt").value;
    
    // Pant measurements
    const pantLength = document.getElementById("length").value;
    const pantKamar = document.getElementById("kamar").value;
    const pantHips = document.getElementById("hips").value;
    const pantWaist = document.getElementById("waist").value;
    const pantGhutna = document.getElementById("Ghutna").value;
    const pantBottom = document.getElementById("Bottom").value;
    const pantSeat = document.getElementById("seat").value;
    
    // Shirt measurements
    const shirtLength = document.getElementById("shirtlength").value;
    const shirtBody = document.getElementById("body").value;
    const shirtLoose = document.getElementById("Loose").value;
    const shirtShoulder = document.getElementById("Shoulder").value;
    const shirtAstin = document.getElementById("Astin").value;
    const shirtcollor = document.getElementById("collor").value;
    const shirtallose = document.getElementById("allose").value;
    // Extra measurments
    const extraLength = document.getElementById("extra-input").value;
    const formData = {
        customerName,
        mobileNo,
        dateIssue,
        deliveryDate,
        garmentType,
        suitQty,
        safariQty,
        pantQty,
        shirtQty,
        totalQty,
        todayDate,
        dueDate,
        totalAmt,
        paymentMode,
        paymentStatus,
        paymentAmount,
        pantMeasurements: {
            pantLength,
            pantKamar,
            pantHips,
            pantWaist,
            pantGhutna,
            pantBottom,
            pantSeat
        },
        shirtMeasurements: {
            shirtLength,
            shirtBody,
            shirtLoose,
            shirtShoulder,
            shirtAstin,
            shirtcollor,
            shirtallose
        },
        extraLength: {
            extraLength
        }
        
    };

    // Submit the form data to the backend
fetch('http://127.0.0.1:5000/api/new-bill', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
})
.then(response => response.json())
.then(result => {
    console.log('Bill created:', result);
    alert('Bill created successfully');

    // Call the saveAndPrint function after the form is successfully submitted
    saveAndPrint();

    // Optionally, reset the form after saving and printing
    // document.getElementById('new-bill-form').reset();
})
.catch(error => {
    console.error('Error creating bill:', error);
    alert('An error occurred while creating the bill.');
});
});



function saveAndPrint() {
    const div1 = document.getElementById('printablearea').cloneNode(true);
    const div2 = document.getElementById('customerbill').cloneNode(true);

    const printWindow = window.open('', '', 'width=800,height=600');

    printWindow.document.write('<html><head><title>Print Bill</title>');
    printWindow.document.write('<style>@media print { .page-break { page-break-before: always; } }</style>');
    printWindow.document.write('</head><body>');

    printWindow.document.write('<h1>New Bill Form</h1>');

    // Create a temporary container and add the cloned elements
    const tempContainer = printWindow.document.createElement('div');
    tempContainer.appendChild(div1);

    // Add the page break using a div with the class 'page-break'
    const pageBreak = printWindow.document.createElement('div');
    pageBreak.classList.add('page-break');
    tempContainer.appendChild(pageBreak);

    tempContainer.appendChild(div2);
    printWindow.document.body.appendChild(tempContainer);

    // printWindow.document.write('<h1>Customer Bill</h1>');
    printWindow.document.write('</body></html>');
    printWindow.document.close();

    // Wait for all images in the new window to load before printing
    const images = printWindow.document.images;
    const totalImages = images.length;
    let imagesLoaded = 0;

    if (totalImages === 0) {
        // If there are no images, proceed to print immediately
        printWindow.focus();
        printWindow.print();
        printWindow.close();
    } else {
        // Wait for all images to load
        for (let i = 0; i < totalImages; i++) {
            images[i].onload = () => {
                imagesLoaded++;
                if (imagesLoaded === totalImages) {
                    // All images are loaded, proceed to print
                    printWindow.focus();
                    printWindow.print();
                    printWindow.close();
                }
            };

            // In case the image fails to load, handle the error and continue
            images[i].onerror = () => {
                imagesLoaded++;
                if (imagesLoaded === totalImages) {
                    // Even with errors, proceed to print after all load attempts
                    printWindow.focus();
                    printWindow.print();
                    printWindow.close();
                }
            };
        }
    }
}



function fetchOrders() {
    fetch('http://127.0.0.1:5000/api/orders')
        .then(response => response.json())
        .then(data => {
            const ordersContainer = document.getElementById('order-overview');
            ordersContainer.innerHTML = ''; // Clear previous content

            if (data && Object.keys(data).length > 0) {
                for (const deliveryDate in data) {
                    const dateHeader = document.createElement('h3');
                    dateHeader.textContent = `Delivery Date: ${deliveryDate}`;
                    ordersContainer.appendChild(dateHeader);

                    const ordersForDate = Array.isArray(data[deliveryDate]) ? data[deliveryDate] : [];

                    let table = `<table>
                        <thead>
                            <tr>
                                <th>Serial No.</th>
                                <th>ID</th>
                                <th>Garment Type</th>
                                <th>Quantity</th>
                                <th>Status</th>
                                <th>Update Status</th>
                                <th>Order Date</th>
                                <th>Payment Mode</th>
                                <th>Payment Status</th>
                                <th>Update Payment Status</th>
                                <th>Payment Amount</th>
                                <th>Bill ID</th>
                            </tr>
                        </thead>
                        <tbody>`;

                    ordersForDate.forEach((order, index) => {
                        const serialNumber = index + 1;
                        table += `<tr>
                            <td>${serialNumber}</td>
                            <td>${order.id}</td>
                            <td>${order.garment_type}</td>
                            <td>${order.quantity}</td>
                            <td>${order.status}</td>
                            <td>
                                <select onchange="updateOrderStatus(${order.id}, this.value)">
                                    <option value="Pending" ${order.status === 'Pending' ? 'selected' : ''}>Pending</option>
                                    <option value="Completed" ${order.status === 'Completed' ? 'selected' : ''}>Completed</option>
                                    <option value="Cancelled" ${order.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                                </select>
                            </td>
                            <td>${order.order_date}</td>
                            <td>${order.payment_mode}</td>
                            <td>${order.payment_status}</td>
                            <td>
                                <select onchange="updatePaymentStatus(${order.id}, this.value)">
                                    <option value="Pending" ${order.payment_status === 'Pending' ? 'selected' : ''}>Pending</option>
                                    <option value="Paid" ${order.payment_status === 'Paid' ? 'selected' : ''}>Paid</option>
                                    <option value="Cancelled" ${order.payment_status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                                </select>
                            </td>
                            <td>${order.payment_amount}</td>
                            <td>${order.bill_id}</td>
                        </tr>`;
                    });

                    table += '</tbody></table>';
                    ordersContainer.innerHTML += table;
                }
            } else {
                ordersContainer.innerHTML = '<p>No orders found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching orders:', error);
            ordersContainer.innerHTML = '<p>Error fetching orders.</p>';
        });
}

// Function to update order status
function updateOrderStatus(orderId, newStatus) {
    fetch(`http://127.0.0.1:5000/api/orders/${orderId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(result => {
        console.log('Order status update response:', result);
        alert('Order status updated successfully');
        // No need to reload the page, just show a success message
    })
    .catch(error => {
        console.error('Error updating order status:', error);
        alert('Error updating order status');
    });
}

// Function to update payment status
function updatePaymentStatus(orderId, newPaymentStatus) {
    fetch(`http://127.0.0.1:5000/api/orders/${orderId}/payment-status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ payment_status: newPaymentStatus })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(result => {
        console.log('Payment status update response:', result);
        alert('Payment status updated successfully');
        // No need to reload the page, just show a success message
    })
    .catch(error => {
        console.error('Error updating payment status:', error);
        alert('Error updating payment status');
    });
}

// document.getElementById('order-overview').addEventListener('click', function () {
//     fetchOrders();
// });


