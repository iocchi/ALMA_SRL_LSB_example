<?php

$SRL_SERVICE_URL = 'http://localhost:8000';

// Funzione helper per le chiamate API
function safeFetchJSON($url) {
    global $SRL_SERVICE_URL;
    $fullUrl = strpos($url, 'http') === 0 ? $url : $SRL_SERVICE_URL . $url;

    // Utilizzo di cURL per una gestione più robusta delle richieste HTTP
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $fullUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5); // Timeout di 5 secondi
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    if (curl_errno($ch)) {
        error_log("cURL Error for $fullUrl: " . curl_error($ch));
        curl_close($ch);
        return null;
    }
    curl_close($ch);

    if ($httpCode !== 200) {
        error_log("HTTP Error for $fullUrl: Code $httpCode");
        return null;
    }

    $data = json_decode($response, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        error_log("JSON Decode Error for $fullUrl: " . json_last_error_msg());
        return null;
    }
    return $data;
}

function getVPNIP() {
    $data = safeFetchJSON('/get_my_vpn_ip');
    return $data['vpn_ip'] ?? '0.0.0.0';
}



// Funzione per recuperare i dati dell'utente
function fetchUserData($vpnIp) {
    $data = safeFetchJSON("/user/by-ip/{$vpnIp}");
    if (!isset($data['user'])) {
        return ['error' => true, 'message' => '<p style="color: #6c757d;">No user data available for IP: ' . htmlspecialchars($vpnIp) . '</p>'];
    }
    $userData = $data['user'];
    $userInfoHTML = '
        <h2 style="margin: 10px 0;">Ciao ' . htmlspecialchars($userData['first_name']) . ' ' . htmlspecialchars($userData['last_name']) . '!</h2>
        <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;"> 
            <span><strong>Email:</strong> ' . htmlspecialchars($userData['email']) . '</span>
            <span><strong>Matricola:</strong> ' . htmlspecialchars($userData['matricola']) . '</span>
            <span><strong>Ruolo:</strong> ' . htmlspecialchars($userData['role']) . '</span>
            <span><strong>Stato:</strong> ' . htmlspecialchars($userData['status']) . '</span>
            <span><strong>IP:</strong> ' . htmlspecialchars($userData['vpn_ip']) . '</span>
    ';
    
    if (!empty($userData['wait_timestamp'])) {
        $userInfoHTML .= '<span><strong>In attesa da:</strong> ' . htmlspecialchars($userData['wait_timestamp']) . '</span>';
    }
    
    if (!empty($userData['lsb_access_timestamp'])) {
        $userInfoHTML .= '<span><strong>Sei entrato nel Lab a:</strong> ' . htmlspecialchars($userData['lsb_access_timestamp']) . '</span>';
    }
    
    if (!empty($userData['booking_end_time'])) {
        $userInfoHTML .= '<span><strong>La connessione sarà attiva fino a:</strong> ' . htmlspecialchars($userData['booking_end_time']) . '</span>';
    }
    
    $userInfoHTML .= '</div>';
    return ['error' => false, 'html' => $userInfoHTML];
}

// Funzione per recuperare gli utenti in attesa
function fetchWaitingUsers() {
    $users = safeFetchJSON('/service/waiting');
    if (!is_array($users) || count($users) === 0) {
        return '<p style="color:#6c757d; text-align:center;">No users waiting</p>';
    }
    $html = '<ul style="list-style:none;padding:0;">';
    foreach ($users as $u) { 
        $html .= '<li style="padding:10px;border-left:4px solid #007bff;margin:8px 0;border-radius:4px;"> <strong>' . htmlspecialchars($u['first_name']) . ' ' . htmlspecialchars($u['last_name']) . '</strong> &nbsp;&nbsp; Matricola: ' . htmlspecialchars($u['matricola']) . ' &nbsp;&nbsp; &nbsp;&nbsp; E-mail: ' . htmlspecialchars($u['email']) . '   &nbsp;&nbsp;  Ruolo: ' . htmlspecialchars($u['role']) . ' <br> In attesa da: ' . htmlspecialchars($u['waiting_since']) . ' </li>';
    }
    $html .= '</ul>';
    return $html;
}

// Funzione per recuperare gli utenti nel lab
function fetchInLabUsers() {
    $users = safeFetchJSON('/service/inlab');
    if (!is_array($users) || count($users) === 0) {
        return '<p style="color:#6c757d; text-align:center;">No users in lab</p>';
    }
    $html = '<ul style="list-style:none;padding:0;">';
    foreach ($users as $u) { 
        $vpnIp = htmlspecialchars($u['vpn_ip'] ?? '');
        $html .= '<li style="padding:10px;border-left:4px solid #28a745;margin:8px 0;border-radius:4px;"> <strong>' . htmlspecialchars($u['first_name']) . ' ' . htmlspecialchars($u['last_name']) . '</strong> &nbsp;&nbsp; Matricola: ' . htmlspecialchars($u['matricola']) . ' &nbsp;&nbsp; &nbsp;&nbsp; E-mail: ' . htmlspecialchars($u['email']) . '   &nbsp;&nbsp;  Ruolo: ' . htmlspecialchars($u['role']) . ' &nbsp;&nbsp; Stato: ' . htmlspecialchars($u['status']) . ' &nbsp;&nbsp; VPN IP: ' . $vpnIp . ' <br> In Lab da: ' . htmlspecialchars($u['lsb_access_timestamp']) . '</li>';
    }
    $html .= '</ul>';
    return $html;
}

// Funzione per recuperare le prenotazioni
function fetchBookings() {
    $bookings = safeFetchJSON('/service/bookings');
    if (!is_array($bookings) || count($bookings) === 0) {
        return '<p style="color:#6c757d; text-align:center;">No bookings</p>';
    }
    $html = '<ul style="list-style:none;padding:0;">';
    foreach ($bookings as $b) { 
        $status = htmlspecialchars($b['status']);
        $statusColor = $status === 'confirmed' ? '#28a745' : ($status === 'expired' ? '#dc3545' : '#ffc107');
        $endTime = $b['end_time'] ? " - " . htmlspecialchars($b['end_time']) : '';
        $html .= '<li style="padding:10px;border-left:4px solid ' . $statusColor . ';margin:8px 0;border-radius:4px;"> 📅 ' . htmlspecialchars($b['start_time']) . $endTime . ' &nbsp;&nbsp; <strong>Booking ID: ' . htmlspecialchars($b['id']) . '</strong> &nbsp;&nbsp; User ID: ' . htmlspecialchars($b['user_id']) . ' &nbsp;&nbsp; Service ID: ' . htmlspecialchars($b['service_id']) . ' &nbsp;&nbsp; Token: ' . htmlspecialchars($b['token']) . ' &nbsp;&nbsp; <span style="color:' . $statusColor . ';font-weight:bold;">Stato: ' . $status . '</span> &nbsp;&nbsp; Slots: ' . htmlspecialchars($b['num_slots']) . '</li>';
    }
    $html .= '</ul>';
    return $html;
}

// Esecuzione delle funzioni per ottenere i dati prima del rendering HTML

$vpnIp = getVPNIP();

$userDataResult = fetchUserData($vpnIp);
$waitingUsersHTML = fetchWaitingUsers();
$inLabUsersHTML = fetchInLabUsers();
$bookingsHTML = fetchBookings();

?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>LSB HTML/PHP</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        body { font-family: sans-serif; margin: 20px; background: #f8f9fa; }
        h1 { text-align: center; }
        .charts { display: flex; flex-wrap: wrap; justify-content: space-around; }
        .chart-box { width: 45%; min-width: 300px; margin: 20px 0; }
        .slider-container { text-align: center; margin: 20px 0; }
        .card { margin: 10px 0; padding: 12px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); }
    </style>
</head>
<body>
    <h1>🔬 Dashboard Esperimento LSB di prova (PHP)</h1>

    <div id="user-data" class="card" style="text-align: center;">
        
        <div id="user-info">
            <?php echo $userDataResult['error'] ? $userDataResult['message'] : $userDataResult['html']; ?>
        </div>

<form method="POST" action="handle_actions.php" style="margin-top: 15px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
            <button type="submit" name="action" value="disconnect" style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold;">
                🔌 Esci dal Lab
            </button>
            <button type="submit" name="action" value="set_available" style="padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold;">
                ✅ Imposta Laboratorio Disponibile
            </button>
            <button type="submit" name="action" value="set_unavailable" style="padding: 10px 20px; background: #ffc107; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold;">
                ⛔ Imposta Laboratorio Non Disponibile
            </button>
        </form>
        
        <!-- div style="margin-top: 15px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
            <button id="disconnect-btn" style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold;">
                🔌 Esci dal Lab
            </button>
            <button id="set-available-btn" style="display: none; padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold;">
                ✅ Imposta Laboratorio Disponibile
            </button>
            <button id="set-unavailable-btn" style="display: none; padding: 10px 20px; background: #ffc107; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold;">
                ⛔ Imposta Laboratorio Non Disponibile
            </button>
        </div -->
        
        <div id="disconnect-message" style="margin-top: 10px;">
            <?php
            if (isset($_GET['status'])) {
                if ($_GET['status'] === 'disconnected') {
                    echo '<p style="color:#28a745;font-weight:bold;">✅ Segnale Esperimento completato inviato.</p>';
                } else if ($_GET['status'] === 'error') {
                     echo '<p style="color:red;font-weight:bold;">❌ Errore nell\'azione.</p>';
                } else if ($_GET['status'] === 'availability_true') {
                     echo '<p style="color:#007bff;font-weight:bold;">✅ Disponibilità Lab aggiornata. Lab disponibile</p>';
                } else if ($_GET['status'] === 'availability_false') {
                     echo '<p style="color:#007bff;font-weight:bold;">⛔ Disponibilità Lab aggiornata. Lab non disponibile</p>';
                }
            }
            ?>
        
        </div>
    </div>

    <br><br><br>
    <h1 aligh=center>Your lab here</h1>
    <br><br><br>

    <div id="inlab-users-section" class="card" style="margin: 20px auto; max-width: 900px;">
        <h3 style="text-align: center; margin-bottom: 10px;">✅ Utenti nel Lab</h3>
        <div id="inlab-users-list">
            <?php echo $inLabUsersHTML; ?>
        </div>
    </div>

    <div id="waiting-users-section" class="card" style="margin: 20px auto; max-width: 900px;">
        <h3 style="text-align: center; margin-bottom: 10px;">👥 Utenti in attesa di entrare nel Lab</h3>
        <div id="waiting-users-list">
            <?php echo $waitingUsersHTML; ?>
        </div>
    </div>

    <div id="bookings-section" class="card" style="margin: 20px auto; max-width: 900px;">
        <h3 style="text-align: center; margin-bottom: 10px;">📅 Prenotazioni del Lab </h3>
        <div id="bookings-list">
            <?php echo $bookingsHTML; ?>
        </div>
    </div>


</body>
</html>
