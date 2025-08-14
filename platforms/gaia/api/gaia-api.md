# GAIA API
**UTCS-MI Code: [536] Gaia API**

## Global Aerospace Intelligence Architecture API

### Mission Management
- `POST /missions` - Create new mission
- `GET /missions/{id}` - Get mission details
- `PUT /missions/{id}` - Update mission
- `GET /missions/{id}/status` - Mission status

### Satellite Control
- `POST /satellites` - Register satellite
- `GET /satellites/{id}` - Satellite telemetry
- `POST /satellites/{id}/commands` - Send commands
- `GET /satellites/{id}/health` - Health status

### Autonomous Operations
- `POST /autonomy/enable/{satellite_id}` - Enable autonomy
- `GET /autonomy/status/{satellite_id}` - Autonomy status
- `POST /autonomy/decisions` - Decision engine interface
- `GET /autonomy/plans` - Planning engine status

### Ground Operations
- `GET /ground-stations` - Available ground stations
- `POST /ground-stations/{id}/connect` - Connect to satellite
- `GET /ground-stations/{id}/schedule` - Contact schedule

### Integration
- **AMOReS Compliance**: Regulatory validation for all operations
- **CaaS Certification**: Automated certification workflows
- **WEE Learning**: Continuous improvement from mission data