V60 fixes the /cases/ 500 caused by legacy quality payloads using
`multiplier` while the response model required `condition_multiplier`.
The schema now accepts both names; the serializer also emits the legacy field
for compatibility. Added check_cases.py. No database reset or destructive migration.
