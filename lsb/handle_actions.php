<?php
// ====================================================================
// CONFIGURAZIONE E FUNZIONI DI SUPPORTO
// ====================================================================

// Configurazione del servizio SRL (deve essere accessibile dal server PHP!)
$SRL_SERVICE_URL = 'http://localhost:8000';

// Funzione helper per ottenere l'IP VPN (come simulato in index.php)
function getVPNIP() {
    // In un sistema reale, questo dovrebbe provenire dalla sessione o da un meccanismo di autenticazione
    return "10.8.0.2"; // Valore fittizio di esempio
}

// Funzione helper per le chiamate API
function safeApiCall($url, $method = 'GET') {
    global $SRL_SERVICE_URL;
    $fullUrl = $SRL_SERVICE_URL . $url;

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $fullUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method); // Setta il metodo (PUT, PATCH, GET, etc.)
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    
    // Esegui la chiamata
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    if ($curlError || $httpCode < 200 || $httpCode >= 300) {
        error_log("API Call Error: URL: $fullUrl, Method: $method, HTTP Code: $httpCode, cURL Error: $curlError, Response: $response");
        return ['success' => false, 'http_code' => $httpCode];
    }

    $data = json_decode($response, true);
    return ['success' => true, 'data' => $data, 'http_code' => $httpCode];
}

// ====================================================================
// LOGICA DI GESTIONE DELLE AZIONI
// ====================================================================

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    
    $action = $_POST['action'];
    $vpnIp = getVPNIP();
    $redirectStatus = 'error'; // Default in caso di fallimento

    switch ($action) {
        case 'disconnect':
            $result = safeApiCall("/api/user/{$vpnIp}/disconnect", 'PUT');
            if ($result['success']) {
                $redirectStatus = 'disconnected';
            }
            break;

        case 'set_available':
            $result = safeApiCall("/api/service/availability/true", 'PATCH');
            if ($result['success']) {
                $redirectStatus = 'availability_true';
            }
            break;

        case 'set_unavailable':
            $result = safeApiCall("/api/service/availability/false", 'PATCH');
            if ($result['success']) {
                $redirectStatus = 'availability_false';
            }
            break;
            
        default:
            // Azione non riconosciuta
            $redirectStatus = 'error';
            break;
    }

    // Reindirizza alla dashboard principale con lo stato aggiornato
    header("Location: index.php?status=" . $redirectStatus);
    // header("Location: index.php");
    exit;

} else {
    // Metodo non POST o campo 'action' mancante
    header("Location: index.php?status=error_invalid_request");
    exit;
}
?>

