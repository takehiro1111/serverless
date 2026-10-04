package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

const (
	slackWebhookURL = "https://hooks.slack.com/services/TODO/TODO/TODO"
	slackChannel    = "#TODO"
	slackUsername   = "sandbox-resource-notify"
)

func buildMessage(accountID string, findings []finding) string {
	var b strings.Builder
	fmt.Fprintf(&b, ":warning: sandbox (%s) にリソースが残っています\n", accountID)
	for _, f := range findings {
		fmt.Fprintf(&b, "\n*%s / %s* (%d)\n", f.Region, f.Service, len(f.IDs))
		for _, id := range f.IDs {
			fmt.Fprintf(&b, "• %s\n", id)
		}
	}
	return b.String()
}

func notifySlack(ctx context.Context, text string) error {
	payload, err := json.Marshal(map[string]string{
		"channel":  slackChannel,
		"username": slackUsername,
		"text":     text,
	})
	if err != nil {
		return fmt.Errorf("marshal slack payload: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, slackWebhookURL, bytes.NewReader(payload))
	if err != nil {
		return fmt.Errorf("build slack request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return fmt.Errorf("post slack webhook: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode/100 != 2 {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("slack webhook returned %d: %s", resp.StatusCode, body)
	}
	return nil
}
