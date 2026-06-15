# test.json permutations & combinations

Variant configs for the BrowserStack GitHub-app test-orchestration source
(`test.json`, referenced from `browserstack.yml` → `source`). The root
`test.json` is the canonical/default config and is left untouched.

Each file maps a **service identifier** (top-level key) to:

| Field          | Meaning                                  |
| -------------- | ---------------------------------------- |
| `url`          | Git repository URL for the service       |
| `baseBranch`   | Branch to diff against                   |
| `featureBranch`| Branch under test                        |

## Service identifier (top-level key) rules

1. **Max length 30 characters.**
2. **ALL CAPS** (no lowercase letters).
3. Only **four special characters** allowed: `_`  `-`  `.`  `/`
   (any other special character or space is invalid).

## Variants

### Number of services
| File | Scenario |
| ---- | -------- |
| `single_service.json` | One service (real repo) |
| `two_services.json`   | Two services (real repo) |
| `multi_services.json` | Five services (mixed real + placeholder repos) |

### Branch combinations
| File | Scenario |
| ---- | -------- |
| `branch_same_base_feature.json` | `baseBranch` == `featureBranch` |
| `branch_varied_features.json`   | Different feature/bugfix/hotfix branches |
| `empty_branch_values.json`      | Empty branch string values + an empty `url` |
| `invalid_branch_values.json`    | Invalid branch values (spaces, illegal git ref, `null`, non-string number) |

### Edge cases (negative testing)
| File | Scenario |
| ---- | -------- |
| `edge_empty_object.json`          | Empty JSON object `{}` |
| `edge_missing_url.json`           | Entry missing `url` |
| `edge_missing_branches.json`      | Entry missing both branches |
| `edge_malformed_invalid_json.json`| Intentionally invalid JSON (trailing comma + missing comma) |

### Key-identifier rule coverage
| File | Scenario |
| ---- | -------- |
| `keys_valid_rules.json`   | Keys that satisfy all rules, incl. a 30-char boundary key |
| `keys_invalid_rules.json` | Keys that violate rules (lowercase, >30 chars, disallowed specials, spaces) |
| `duplicate_key_values.json` | Same key identifier repeated — the last occurrence should win |

> `keys_invalid_rules.json` uses `_comment` fields to explain each violation.
> `edge_malformed_invalid_json.json` is deliberately **not** valid JSON — it
> will fail a JSON parse, which is the point of that fixture.

## Using a variant

Point `browserstack.yml` at the variant you want to exercise:

```yaml
source: 'test_configs/two_services.json'
```
