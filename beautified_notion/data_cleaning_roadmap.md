# 📋 Database Cleaning & Labeling: Strategy Roadmap

This roadmap identifies data anomalies, outlines data validation methods, and outlines a step-by-step strategy for preparing bid-ask datasets to train predictive models.

---

## 🔍 1. Current Data Quality Issues

While our bid and ask price telemetry is generally consistent, we have identified several core data issues that must be addressed:

### 1.1 Outlier Volumetric Samples (Bid-Ask Extremes)
*   **The Issue:** Several records contain extremely high or low bid-ask prices paired with a transaction volume of exactly 1.
*   **Impact:** If left uncorrected, these highly volatile, low-density outliers distort regression modeling scales.
*   **Remedy:** Filter out low-volume transactions ($Size = 1$) that deviate by more than $\pm 3$ standard deviations from the moving average price.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/15883252-8baf-4cd3-9fd6-2cc4c6ca772a/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZXS4RT7U%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223906Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDInptv6nuXFrbtSPsDb2SYiBJYAqWpsaa3f0UsWCEOHAIhANOc2yGG4b48AcPyS2Lw2c5FoTqxKIYkfwbbPx6WVJeRKogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgwMVbrRAdlHd0zJEn4q3AMQRm%2BHlLxWsv0zOPZUStAlpQaflvECwJnSQheUl%2FbMsz3DNYf0oa175p1yueuo27YluWaKkJ4AZjoj4EdwSah9L2z9VuH6SV%2BAfCsQ7C%2FUPxU1iD7cvRJXS5UJUvMQmVKaeyFxJt%2FSNJdWMjTdcEs1xUBgE7wWg%2FFo7H6n%2FFU0j1cyuWAGKVMsdwttgRSxy9RiMU9E%2By5PkAfszNM0GG1D67FR4lJRJnWDYfA0fpdpk9OhgN0UvAUbStAaZwTmowiVe%2BiR%2F6U9D5y2Ws%2FYdCWXfKfSHHbrAzz2yzUHXfFlCYMaF6cTrs38vl83UwyYA9PYk8FogS7Dq3Iu95KlRm0vB2lMjj3jslb2jvPhrWb15Ap2wW%2FJ0rAI9WnXBvA3sXlc%2B7IDtRhXdIVr5KzcCrRvedlPHgjH2Wp1Tj2tK8Tc4Nhp2oBYgHWkkxkUaZ5zlUI1C7iaf20jx%2Fc7CCu6wqX1fl9%2Fy1oJG%2FWV1JN%2BBrytxxb8e32f2Ia6T8x44AnPl9KwzxquXX1OpMh6508XpD6IchQ8PLGJ5cSleAFz610Y0DraE%2BrZpgU4C%2BH5wcoHCD8tNb%2B8bGpIbvknvQjl71FBNRV5VDaIRh04dTk30PTC4PULM1tWtCGWXUGelTDO15fRBjqkAbCqwtmPvcKecKIwAzEZuFg4CLIW8IyhwEkEehC30fxbGtTyjPAzmz0pjElDZD%2FNey71JQpSTHH4AlopqAYh2%2BrZYts%2F8RwiEP7wpK2vtjjZ9pJYXA3h5hVxxZtbVPtyGjhT5N3sRAAOuRdFPSK4OM19HXk%2BShiXHy6SlToGZ69RtNsUBKVxihO7ivam%2FfDGcU0WIl9MeHAOzAC6tmzSV1dxM5jF&X-Amz-Signature=e19563b3a75f81436f3b582382dc902f6ead5553d02322f98429ce13337a83a9&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

### 1.2 Telemetry Gaps (Missing Column Values)
*   **The Issue:** Gaps in specific time-series rows lead to null inputs during network execution.
*   **Remedy:** Apply forward-fill imputation for real-time streaming segments (assuming temporal price stability), or use linear interpolation for short gaps.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/078ec059-2fd1-4e29-af71-585ac9e331a1/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZXS4RT7U%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223906Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDInptv6nuXFrbtSPsDb2SYiBJYAqWpsaa3f0UsWCEOHAIhANOc2yGG4b48AcPyS2Lw2c5FoTqxKIYkfwbbPx6WVJeRKogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgwMVbrRAdlHd0zJEn4q3AMQRm%2BHlLxWsv0zOPZUStAlpQaflvECwJnSQheUl%2FbMsz3DNYf0oa175p1yueuo27YluWaKkJ4AZjoj4EdwSah9L2z9VuH6SV%2BAfCsQ7C%2FUPxU1iD7cvRJXS5UJUvMQmVKaeyFxJt%2FSNJdWMjTdcEs1xUBgE7wWg%2FFo7H6n%2FFU0j1cyuWAGKVMsdwttgRSxy9RiMU9E%2By5PkAfszNM0GG1D67FR4lJRJnWDYfA0fpdpk9OhgN0UvAUbStAaZwTmowiVe%2BiR%2F6U9D5y2Ws%2FYdCWXfKfSHHbrAzz2yzUHXfFlCYMaF6cTrs38vl83UwyYA9PYk8FogS7Dq3Iu95KlRm0vB2lMjj3jslb2jvPhrWb15Ap2wW%2FJ0rAI9WnXBvA3sXlc%2B7IDtRhXdIVr5KzcCrRvedlPHgjH2Wp1Tj2tK8Tc4Nhp2oBYgHWkkxkUaZ5zlUI1C7iaf20jx%2Fc7CCu6wqX1fl9%2Fy1oJG%2FWV1JN%2BBrytxxb8e32f2Ia6T8x44AnPl9KwzxquXX1OpMh6508XpD6IchQ8PLGJ5cSleAFz610Y0DraE%2BrZpgU4C%2BH5wcoHCD8tNb%2B8bGpIbvknvQjl71FBNRV5VDaIRh04dTk30PTC4PULM1tWtCGWXUGelTDO15fRBjqkAbCqwtmPvcKecKIwAzEZuFg4CLIW8IyhwEkEehC30fxbGtTyjPAzmz0pjElDZD%2FNey71JQpSTHH4AlopqAYh2%2BrZYts%2F8RwiEP7wpK2vtjjZ9pJYXA3h5hVxxZtbVPtyGjhT5N3sRAAOuRdFPSK4OM19HXk%2BShiXHy6SlToGZ69RtNsUBKVxihO7ivam%2FfDGcU0WIl9MeHAOzAC6tmzSV1dxM5jF&X-Amz-Signature=4969cbe5243533a6487311126aad606ccfcfc2cc222c5199e2a466f782f19826&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

---

## ⚙️ 2. The Resolution & Extraction Pipeline

```mermaid
graph TD
    Raw[1. Raw Bid-Ask Telemetry] --> Filter[2. Volume-Weighted IQR Filter]
    Filter --> Impute[3. Temporal Linear Interpolation]
    Impute --> Normal[4. Z-Score Scaling & Normalization]
    Normal --> Output[5. Training Dataset]
```

### 2.1 Cleaning Steps
1.  **Volume-Weighted Outlier Filtering:** Use Interquartile Range (IQR) filtering restricted by volume weights to isolate and strip out low-density, highly volatile outlier prices.
2.  **Imputation:** Implement an automated pipeline that checks missing row footprints, forward-fills database rows for gaps shorter than 3 periods, and uses linear interpolation for larger gaps.
3.  **Z-Score Normalization:** Apply Z-score scaling across active features (such as bid/ask prices, moving averages, and rolling volatilities) to standardize training inputs.
