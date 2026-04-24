export type RuleHit = {
  id: number;
  email_id: number;
  rule_name: string;
  score_delta: number;
  reason: string | null;
  created_at: string;
};

export type StoredEmail = {
  id: number;
  sender: string;
  recipient: string;
  subject: string;
  body: string;
  score: number;
  verdict: string;
  created_at: string;
};

export type EmailDetails = StoredEmail & {
  rule_hits: RuleHit[];
};

export type ListEntry = {
  id: number;
  list_type: string;
  value: string;
  created_at: string;
};
