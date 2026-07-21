# Sample API (fictional)

### Basic

| Item | Value |
|------|-------|
| Name | Query series conclusion |
| Method | GET |
| Path | `/common/api/seriesConclusionDesc` |
| Base URL (example) | `https://api.example.com` |

### Query params

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| version | String | Yes | Client version |
| deviceType | Integer | Yes | 1=iOS, 2=Android, 3=Harmony, 4=H5 |
| seriesId | String | Yes | Series id |

### Success

```json
{
  "returncode": 0,
  "message": "Success",
  "data": {
    "seriesId": "1001",
    "conclusionDesc": "Example balanced conclusion for demonstration only."
  }
}
```

### Errors

| returncode | message | When |
|------------|---------|------|
| 0 | Success | OK |
| 400 | version is invalid | version empty |
| 400 | deviceType is invalid | deviceType empty or <= 0 |
| 400 | seriesId is invalid | seriesId empty |
| 500 | system error | server fault |
