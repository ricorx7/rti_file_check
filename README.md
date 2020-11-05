# File Check
Check the Binary or DB file for any errors in the data.
This will check things like voltage, heading, pitch and roll spikes, date jumps and other test.
Streamlit is used to display plots of the results.

![File Check Loading](http://rowetechinc.co/github_img/file-check-loading.png)

![File Check Summary](http://rowetechinc.co/github_img/file-check-report.png)

![File Check Streamlit](http://rowetechinc.co/github_img/file-check-streamlit.png)

# Install requirements

```commandline
pip install -r requirements.txt
pip install -r rti_python\requirements.txt
pip install -r rti_python_plot\requirements.txt
```

# Run Application
```commandline
# To just see results
python app.py

# To see plots also
streamlit run app.py
```