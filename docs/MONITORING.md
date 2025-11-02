# Monitoring & Analytics Setup

Comprehensive guide for setting up monitoring, analytics, and alerting for Places2Go.

## Table of Contents

1. [Overview](#overview)
2. [Application Insights](#application-insights)
3. [Google Analytics](#google-analytics)
4. [Uptime Monitoring](#uptime-monitoring)
5. [Performance Monitoring](#performance-monitoring)
6. [Alert Configuration](#alert-configuration)
7. [Dashboard Setup](#dashboard-setup)

## Overview

### Monitoring Stack

| Component | Purpose | Cost |
|-----------|---------|------|
| Application Insights | Error tracking, performance | Free tier: 5GB/month |
| Google Analytics 4 | User behavior, traffic | Free |
| UptimeRobot | Uptime monitoring | Free: 50 monitors |
| Azure Monitor | Infrastructure health | Included with Azure |

### Success Metrics (from Phase 4D)

- ✅ Zero-downtime deployments
- ✅ < 5 minute deploy time
- ✅ 99.9% uptime
- ✅ Automated rollback on failures
- ✅ Monitoring alerts working

## Application Insights

Azure Application Insights provides real-time application performance monitoring.

### Setup

#### 1. Create Application Insights Resource

**Using Azure Portal:**

1. Go to https://portal.azure.com
2. Search for "Application Insights"
3. Click "Create"
4. Fill in details:
   - **Name**: places2go-insights
   - **Resource Group**: places2go-rg (same as Static Web App)
   - **Region**: Same as your Static Web App
   - **Workspace**: Create new or use existing

5. Click "Review + create"

**Using Azure CLI:**

```bash
# Create Application Insights
az monitor app-insights component create \
  --app places2go-insights \
  --location eastus \
  --resource-group places2go-rg \
  --application-type web \
  --retention-time 90

# Get connection string
APPINSIGHTS_CONNECTION_STRING=$(az monitor app-insights component show \
  --app places2go-insights \
  --resource-group places2go-rg \
  --query "connectionString" -o tsv)

echo $APPINSIGHTS_CONNECTION_STRING
```

#### 2. Add Connection String to GitHub

1. Copy the connection string
2. Go to GitHub repository → Settings → Secrets
3. Add secret:
   - Name: `APPLICATIONINSIGHTS_CONNECTION_STRING`
   - Value: [paste connection string]

#### 3. Enable in Configuration

Update `config/.env.production`:

```env
ENABLE_APPLICATION_INSIGHTS=True
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=...
```

#### 4. Add Tracking Script

Create `deployment/insights.html` snippet:

```html
<!-- Application Insights -->
<script type="text/javascript">
  !function(T,l,y){var S=T.location,k="script",D="instrumentationKey",C="ingestionendpoint",I="disableExceptionTracking",E="ai.device.",b="toLowerCase",w="crossOrigin",N="POST",e="appInsightsSDK",t=y.name||"appInsights";(y.name||T[e])&&(T[e]=t);var n=T[t]||function(d){var g=!1,f=!1,m={initialize:!0,queue:[],sv:"5",version:2,config:d};function v(e,t){var n={},a="Browser";return n[E+"id"]=a[b](),n[E+"type"]=a,n["ai.operation.name"]=S&&S.pathname||"_unknown_",n["ai.internal.sdkVersion"]="javascript:snippet_"+(m.sv||m.version),{time:function(){var e=new Date;function t(e){var t=""+e;return 1===t.length&&(t="0"+t),t}return e.getUTCFullYear()+"-"+t(1+e.getUTCMonth())+"-"+t(e.getUTCDate())+"T"+t(e.getUTCHours())+":"+t(e.getUTCMinutes())+":"+t(e.getUTCSeconds())+"."+((e.getUTCMilliseconds()/1e3).toFixed(3)+"").slice(2,5)+"Z"}(),iKey:e,name:"Microsoft.ApplicationInsights."+e.replace(/-/g,"")+"."+t,sampleRate:100,tags:n,data:{baseData:{ver:2}}}}var h=d.url||y.src;if(h){function a(e){var t,n,a,i,r,o,s,c,u,p,l;g=!0,m.queue=[],f||(f=!0,t=h,s=function(){var e={},t=d.connectionString;if(t)for(var n=t.split(";"),a=0;a<n.length;a++){var i=n[a].split("=");2===i.length&&(e[i[0][b]()]=i[1])}if(!e[C]){var r=e.endpointsuffix,o=r?e.location:null;e[C]="https://"+(o?o+".":"")+"dc."+(r||"services.visualstudio.com")}return e}(),c=s[D]||d[D]||"",u=s[C],p=u?u+"/v2/track":d.endpointUrl,(l=[]).push((n="SDK LOAD Failure: Failed to load Application Insights SDK script (See stack for details)",a=t,i=p,(o=(r=v(c,"Exception")).data).baseType="ExceptionData",o.baseData.exceptions=[{typeName:"SDKLoadFailed",message:n.replace(/\./g,"-"),hasFullStack:!1,stack:n+"\nSnippet failed to load ["+a+"] -- Telemetry is disabled\nHelp Link: https://go.microsoft.com/fwlink/?linkid=2128109\nHost: "+(S&&S.pathname||"_unknown_")+"\nEndpoint: "+i,parsedStack:[]}],r)),l.push(function(e,t,n,a){var i=v(c,"Message"),r=i.data;r.baseType="MessageData";var o=r.baseData;return o.message='AI (Internal): 99 message:"'+("SDK LOAD Failure: Failed to load Application Insights SDK script (See stack for details) ("+n+")").replace(/\"/g,"")+'"',o.properties={endpoint:a},i}(0,0,t,p)),function(e,t){if(JSON){var n=T.fetch;if(n&&!y.useXhr)n(t,{method:N,body:JSON.stringify(e),mode:"cors"});else if(XMLHttpRequest){var a=new XMLHttpRequest;a.open(N,t),a.setRequestHeader("Content-type","application/json"),a.send(JSON.stringify(e))}}}(l,p))}function i(e,t){f||setTimeout(function(){!t&&m.core||a()},500)}var e=function(){var n=l.createElement(k);n.src=h;var e=y[w];return!e&&""!==e||"undefined"==n[w]||(n[w]=e),n.onload=i,n.onerror=a,n.onreadystatechange=function(e,t){"loaded"!==n.readyState&&"complete"!==n.readyState||i(0,t)},n}();y.ld<0?l.getElementsByTagName("head")[0].appendChild(e):setTimeout(function(){l.getElementsByTagName(k)[0].parentNode.appendChild(e)},y.ld||0)}try{m.cookie=l.cookie}catch(p){}function t(e){for(;e.length;)!function(t){m[t]=function(){var e=arguments;g||m.queue.push(function(){m[t].apply(m,e)})}}(e.pop())}var n="track",r="TrackPage",o="TrackEvent";t([n+"Event",n+"PageView",n+"Exception",n+"Trace",n+"DependencyData",n+"Metric",n+"PageViewPerformance","start"+r,"stop"+r,"start"+o,"stop"+o,"addTelemetryInitializer","setAuthenticatedUserContext","clearAuthenticatedUserContext","flush"]),m.SeverityLevel={Verbose:0,Information:1,Warning:2,Error:3,Critical:4};var s=(d.extensionConfig||{}).ApplicationInsightsAnalytics||{};if(!0!==d[I]&&!0!==s[I]){var c="onerror";t(["_"+c]);var u=T[c];T[c]=function(e,t,n,a,i){var r=u&&u(e,t,n,a,i);return!0!==r&&m["_"+c]({message:e,url:t,lineNumber:n,columnNumber:a,error:i}),r},d.autoExceptionInstrumented=!0}return m}(y.cfg);function a(){y.onInit&&y.onInit(n)}(T[t]=n).queue&&0===n.queue.length?(n.queue.push(a),n.trackPageView({})):a()}(window,document,{
    src: "https://js.monitor.azure.com/scripts/b/ai.2.min.js",
    crossOrigin: "anonymous",
    cfg: {
      connectionString: "YOUR_CONNECTION_STRING_HERE"
    }
  });
</script>
```

### Metrics to Monitor

#### Performance Metrics
- Page load time
- Time to interactive
- First contentful paint
- Largest contentful paint

#### Usage Metrics
- Page views
- Unique users
- Session duration
- User flows

#### Error Metrics
- JavaScript exceptions
- Failed HTTP requests
- Console errors
- Unhandled promise rejections

### Custom Events

Track custom events in your visualizations:

```javascript
// Track visualization interactions
appInsights.trackEvent({
  name: "VisualizationViewed",
  properties: {
    chartType: "flight_prices",
    destination: "Tokyo"
  }
});

// Track errors
try {
  // Your code
} catch (error) {
  appInsights.trackException({
    exception: error,
    properties: {
      component: "weather_forecast"
    }
  });
}
```

## Google Analytics

Google Analytics 4 provides user behavior insights.

### Setup

#### 1. Create GA4 Property

1. Go to https://analytics.google.com
2. Click "Admin" (gear icon)
3. Click "Create Property"
4. Enter property details:
   - **Property name**: Places2Go
   - **Time zone**: Your timezone
   - **Currency**: Your currency
5. Fill in business information
6. Accept terms of service

#### 2. Get Measurement ID

1. In GA4 property, go to "Data Streams"
2. Click "Add stream" → "Web"
3. Enter website URL
4. Click "Create stream"
5. Copy Measurement ID (G-XXXXXXXXXX)

#### 3. Add to GitHub Secrets

1. Go to GitHub repository → Settings → Secrets
2. Add secret:
   - Name: `GOOGLE_ANALYTICS_ID`
   - Value: G-XXXXXXXXXX

#### 4. Add Tracking Code

Create `deployment/analytics.html`:

```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX', {
    'cookie_flags': 'SameSite=None;Secure',
    'anonymize_ip': true
  });
</script>
```

### Events to Track

#### Page Views (Automatic)
- README page views
- Visualization page views
- Navigation between pages

#### Custom Events

```javascript
// Track downloads
gtag('event', 'download', {
  'event_category': 'engagement',
  'event_label': 'data_export'
});

// Track visualization interactions
gtag('event', 'visualization_interact', {
  'chart_type': 'flight_prices',
  'interaction_type': 'filter'
});

// Track search
gtag('event', 'search', {
  'search_term': 'Tokyo'
});
```

## Uptime Monitoring

UptimeRobot monitors application availability.

### Setup

#### 1. Create Account

1. Go to https://uptimerobot.com
2. Sign up for free account (50 monitors included)

#### 2. Add Monitor

1. Click "Add New Monitor"
2. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Places2Go Production
   - **URL**: https://places2go.azurestaticapps.net
   - **Monitoring Interval**: 5 minutes (free tier)
   - **Keyword**: Optional (e.g., "Places2Go" in page)

3. Click "Create Monitor"

#### 3. Set Up Alerts

1. Go to "My Settings"
2. Add alert contacts:
   - **Email**: your-email@example.com
   - **Slack**: Connect Slack workspace
   - **SMS**: Add phone number (paid)

3. Configure alert thresholds:
   - Alert when down
   - Alert after 5 minutes of downtime
   - Re-alert every 30 minutes

#### 4. Create Status Page (Optional)

1. Click "Status Pages"
2. Create new public status page
3. Add your monitors
4. Customize design
5. Share URL: https://stats.uptimerobot.com/XXXXXX

### Monitors to Create

1. **Production Homepage**
   - URL: https://places2go.azurestaticapps.net
   - Interval: 5 minutes
   - Keyword: "Places2Go"

2. **Key Visualizations**
   - URL: https://places2go.azurestaticapps.net/destinations_map.html
   - Interval: 10 minutes

3. **API Endpoint** (if applicable)
   - URL: https://places2go.azurestaticapps.net/api/health
   - Interval: 5 minutes

## Performance Monitoring

### Web Vitals Tracking

Monitor Core Web Vitals with GA4:

```html
<script type="module">
  import {onCLS, onFID, onLCP, onFCP, onTTFB} from 'https://unpkg.com/web-vitals?module';

  function sendToAnalytics(metric) {
    gtag('event', metric.name, {
      value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
      event_category: 'Web Vitals',
      event_label: metric.id,
      non_interaction: true,
    });
  }

  onCLS(sendToAnalytics);
  onFID(sendToAnalytics);
  onLCP(sendToAnalytics);
  onFCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
</script>
```

### Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Largest Contentful Paint (LCP) | < 2.5s | 🟢 Good |
| First Input Delay (FID) | < 100ms | 🟢 Good |
| Cumulative Layout Shift (CLS) | < 0.1 | 🟢 Good |
| Time to First Byte (TTFB) | < 600ms | 🟢 Good |
| Total Page Size | < 5MB | 🟢 Good |

## Alert Configuration

### Application Insights Alerts

#### 1. Create Alert Rule

```bash
# Create action group for notifications
az monitor action-group create \
  --name places2go-alerts \
  --resource-group places2go-rg \
  --short-name p2galerts \
  --email-receiver admin --email admin@example.com

# Create alert for failed requests
az monitor metrics alert create \
  --name high-failed-requests \
  --resource-group places2go-rg \
  --scopes /subscriptions/XXX/resourceGroups/places2go-rg/providers/Microsoft.Web/sites/places2go \
  --condition "avg requests/failed > 5" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action places2go-alerts \
  --description "Alert when failed requests exceed threshold"
```

#### 2. Alert Types

| Alert | Condition | Action |
|-------|-----------|--------|
| High Error Rate | > 5 errors/min | Email team |
| Slow Response | > 3s avg | Notify ops |
| High CPU | > 80% for 5min | Scale up |
| Low Availability | < 99% | Page on-call |

### Slack Integration

Set up Slack notifications:

1. **Create Slack App**
   - Go to https://api.slack.com/apps
   - Create new app
   - Add Incoming Webhook

2. **Add Webhook to Azure**
   ```bash
   az monitor action-group create \
     --name slack-alerts \
     --resource-group places2go-rg \
     --short-name slackalert \
     --webhook-receiver slack \
     --webhook-url https://hooks.slack.com/services/XXX/YYY/ZZZ
   ```

3. **Configure Alert Messages**
   ```json
   {
     "text": "🚨 Alert: {{ alert.name }}",
     "attachments": [{
       "color": "danger",
       "fields": [
         {"title": "Environment", "value": "Production"},
         {"title": "Severity", "value": "{{ alert.severity }}"},
         {"title": "Description", "value": "{{ alert.description }}"}
       ]
     }]
   }
   ```

## Dashboard Setup

### Azure Dashboard

Create monitoring dashboard:

1. **Create Dashboard**
   - Go to Azure Portal
   - Click "Dashboard"
   - Click "New dashboard"
   - Name: "Places2Go Monitoring"

2. **Add Tiles**
   - Application Insights metrics
   - Static Web App status
   - Deployment history
   - Alert summary

3. **Pin Important Metrics**
   - Failed requests
   - Response time
   - User sessions
   - Deployment status

### Grafana Dashboard (Optional)

For advanced monitoring:

```yaml
# docker-compose.yml
version: '3'
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana-data:/var/lib/grafana
```

## Monitoring Checklist

### Daily
- [ ] Check Application Insights for errors
- [ ] Review uptime status (should be 100%)
- [ ] Check performance metrics
- [ ] Review user analytics

### Weekly
- [ ] Analyze user behavior trends
- [ ] Review slow queries/pages
- [ ] Check alert noise (too many/few?)
- [ ] Update monitoring documentation

### Monthly
- [ ] Review monitoring costs
- [ ] Audit alert effectiveness
- [ ] Update performance targets
- [ ] Conduct monitoring review meeting

## Troubleshooting Monitoring

### No Data in Application Insights

1. **Check connection string**
   - Verify in Azure Portal
   - Check GitHub secrets

2. **Verify tracking code**
   - Check browser console for errors
   - Look for Application Insights requests in Network tab

3. **Check sampling rate**
   - May need to wait for data aggregation
   - Check sampling settings in Azure

### Uptime Alerts Too Frequent

1. **Adjust thresholds**
   - Increase timeout
   - Add retry logic

2. **Check false positives**
   - Verify site is actually down
   - Check from different locations

3. **Review monitor configuration**
   - Correct URL
   - Proper keyword matching

## Best Practices

1. **Start Simple**
   - Begin with basic uptime monitoring
   - Add complexity as needed

2. **Alert Fatigue**
   - Don't alert on everything
   - Tune thresholds to reduce noise

3. **Regular Review**
   - Weekly review of metrics
   - Monthly audit of alerts

4. **Documentation**
   - Document what each alert means
   - Provide runbooks for common issues

5. **Test Alerts**
   - Periodically test alert channels
   - Verify on-call rotations work

## Resources

- [Application Insights Documentation](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [Google Analytics 4 Help](https://support.google.com/analytics/answer/10089681)
- [UptimeRobot API](https://uptimerobot.com/api/)
- [Web Vitals](https://web.dev/vitals/)

---

**Last Updated**: [Date]
**Owner**: DevOps Team
**Review Frequency**: Monthly
