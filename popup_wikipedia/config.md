### Wiki Popup Add-on For Anki

Please note that the following settings do not sync and require a restart to apply:
- `popup_type` (string): Type of popup. 'mobile' for mobile, 'extract' for much shorter extract. Default: `"mobile"`
- `show_notfound_msg` (true/false): Show not found info message if no wikipedia entry is found. Default `true` 
- `popup_hotkey` (string): Hotkey to invoke popup manually. Default: `"Ctrl+Shift+W"`
- `wikipedia_lang` (string): Language of wikipedia to use. Default `"en"`
- `exclude_list` (string): (Optional) Path to list of words to exclude from wikipedia lookups. Default `""` (empty)
- `max_results_limit` (integer): Number of results above which to show a warning on the potential slowdowns they could cause. Set to `0` to disable warning. Default: `1000`.
